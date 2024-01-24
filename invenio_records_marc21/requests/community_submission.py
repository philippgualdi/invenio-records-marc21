# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2024 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Marc21 Community submission request."""

from invenio_rdm_records.requests import CommunitySubmission
from invenio_rdm_records.requests.community_submission import (
    AcceptAction,
    CancelAction,
    DeclineAction,
    ExpireAction,
)
from invenio_requests.customizations import actions

from ..proxies import current_records_marc21 as service


#
# Actions
#
class SubmitAction(actions.SubmitAction):
    """Submit action."""

    def execute(self, identity, uow):
        """Execute the submit action."""
        draft = self.request.topic.resolve()
        service.records_service._validate_draft(identity, draft)
        # Set the record's title as the request title.
        fields = draft.metadata.get("fields",None)
        self.request["title"] = str(fields.get("245", "No Title")) if fields is not None else "NO Title"
        super().execute(identity, uow)

#
# Request
#
class Marc21CommunitySubmission(CommunitySubmission):
    """Review request for submitting a record to a community."""
    type_id = "marc21-community-submission"
    allowed_topic_ref_types = ["marcrecord"]

    available_actions = {
        "create": actions.CreateAction,
        "submit": SubmitAction,
        "delete": actions.DeleteAction,
        "accept": AcceptAction,
        "decline": DeclineAction,
        "cancel": CancelAction,
        "expire": ExpireAction,
    }
