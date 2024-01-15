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


from flask import current_app
from invenio_rdm_records.requests.community_inclusion import CommunityInclusion
from invenio_rdm_records.requests.community_submission import CommunitySubmission
from invenio_rdm_records.services.community_inclusion import CommunityInclusionService


class Marc21CommunityInclusionService(CommunityInclusionService):
    """Service for including a record in a community.

    The Marc21 Requests service wraps some operations of the generic requests service,
    implementing Marc21 business logic.

    Note: this service is meant to be used by other services, and not by a resource.
    The uow should be passed by the caller.
    """

    @property
    def supported_types(self):
        """Supported request types."""
        types = {CommunitySubmission.type_id, CommunityInclusion.type_id}
        types.update(current_app.config.get("MARC21_RECORD_REVIEWS", []))
        return types
