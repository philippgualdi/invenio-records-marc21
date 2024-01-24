# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2024 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Marc21 Review Service."""

from flask import current_app
from invenio_drafts_resources.services.records.uow import ParentRecordCommitOp
from invenio_i18n import lazy_gettext as _
from invenio_notifications.services.uow import NotificationOp
from invenio_rdm_records.notifications.builders import (
    CommunityInclusionNotificationBuilder,
)
from invenio_rdm_records.services.errors import ReviewNotFoundError
from invenio_rdm_records.services.review import ReviewService
from invenio_records_resources.services.uow import RecordIndexOp, unit_of_work
from marshmallow import ValidationError

from ...proxies import current_records_marc21
from ...requests.decorators import request_next_link


class Marc21CommunityInclusionNotificationBuilder(CommunityInclusionNotificationBuilder):

    type = "marc21-community-submission"

class Marc21ReviewService(ReviewService):
    """Marc21 Record review service.

    The review service is in charge of creating a review request.

    The request service is in charge of checking if an identity has permission
    to a given receiver (e.g. a restricted community).

    The request service validates if a receiver/topic is allowed for a given
    request type.

    A request type action is in charge of checking further properties - e.g.
    the submit action can check if the member policy of a community is open or
    closed.
    """

    @property
    def supported_types(self):
        """Supported review types."""
        return current_app.config.get("MARC21_RECORD_REVIEWS", [])

    @request_next_link()
    @unit_of_work()
    def submit(self, identity, id_, data=None, require_review=False, uow=None):
        """Submit record for review or direct publish to the community."""
        if not isinstance(require_review, bool):
            raise ValidationError(
                _("Must be a boolean, true or false"),
                field_name="require_review",
            )

        draft = self.draft_cls.pid.resolve(id_, registered_only=False)
        # Preconditions
        if draft.parent.review is None:
            raise ReviewNotFoundError()

        request_type = draft.parent.review.get_object()["type"]
        self._validate_request_type(request_type)

        # since it is submit review action, assume the receiver is community
        community = draft.parent.review.receiver.resolve()

        # Check permission
        self.require_permission(identity, "update_draft", record=draft)

        # create review request
        request_item = current_records_marc21.community_inclusion_service.submit(
            identity, draft, community, draft.parent.review, data, uow
        )
        request = request_item._request

        # This shouldn't be required BUT because of the caching mechanism
        # in the review systemfield, the review should be set with the updated
        # request object
        draft.parent.review = request
        uow.register(ParentRecordCommitOp(draft.parent))

        if not require_review:
            request_item = current_records_marc21.community_inclusion_service.include(
                identity, community, request, uow
            )

        uow.register(
            NotificationOp(
                Marc21CommunityInclusionNotificationBuilder.build(
                    request_item._request,
                )
            )
        )
        uow.register(RecordIndexOp(draft, indexer=self.indexer))
        return request_item
