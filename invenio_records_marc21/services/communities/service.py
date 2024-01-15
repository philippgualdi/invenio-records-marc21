# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2024 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Marc21 Record Communities Service."""

from invenio_communities.proxies import current_communities
from invenio_rdm_records.requests import CommunityInclusion
from invenio_rdm_records.services.communities import RecordCommunitiesService
from invenio_rdm_records.services.errors import (
    CommunityAlreadyExists,
    OpenRequestAlreadyExists,
)
from invenio_requests import current_request_type_registry, current_requests_service
from invenio_requests.resolvers.registry import ResolverRegistry

from ...proxies import current_records_marc21


class Marc21RecordCommunitiesService(RecordCommunitiesService):
    """Marc21 community record service."""

    def _include(self, identity, community_id, comment, require_review, record, uow):
        """Create request to add the community to the record."""
        # check if the community exists
        community = current_communities.service.record_cls.pid.resolve(community_id)
        com_id = str(community.id)

        already_included = com_id in record.parent.communities
        if already_included:
            raise CommunityAlreadyExists()

        # check if there is already an open request, to avoid duplications
        existing_request_id = self._exists(identity, com_id, record)

        if existing_request_id:
            raise OpenRequestAlreadyExists(existing_request_id)

        type_ = current_request_type_registry.lookup(CommunityInclusion.type_id)
        receiver = ResolverRegistry.resolve_entity_proxy(
            {"community": com_id}
        ).resolve()

        request_item = current_requests_service.create(
            identity,
            {},
            type_,
            receiver,
            topic=record,
            uow=uow,
        )

        # create review request
        request_item = current_records_marc21.community_inclusion_service.submit(
            identity, record, community, request_item._request, comment, uow
        )
        # include directly when allowed
        if not require_review:
            request_item = current_records_marc21.community_inclusion_service.include(
                identity, community, request_item._request, uow
            )
        return request_item
