# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2024 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Marc21 Record Communities config Service."""

from invenio_indexer.api import RecordIndexer
from invenio_rdm_records.services import RDMRecordCommunitiesConfig
from invenio_rdm_records.services.schemas.parent import CommunitiesSchema
from invenio_rdm_records.services.schemas.record_communities import (
    RecordCommunitiesSchema,
)
from invenio_records_resources.services.base.config import FromConfig

from ...records import Marc21Record
from .. import Marc21RecordPermissionPolicy


class Marc21RecordCommunitiesConfig(RDMRecordCommunitiesConfig):
    """Record communities service config."""

    service_id = "record-communities"

    record_cls = Marc21Record
    permission_policy_cls = FromConfig(
        "MARC21_PERMISSION_POLICY",
        default=Marc21RecordPermissionPolicy,
        import_string=True,
    )

    schema = RecordCommunitiesSchema
    communities_schema = CommunitiesSchema

    indexer_cls = RecordIndexer
    indexer_queue_name = service_id
    index_dumper = None

    # Max n. communities that can be added at once
    max_number_of_additions = 10
    # Max n. communities that can be removed at once
    max_number_of_removals = 10
