# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


"""Marc21 Record Service config."""

from invenio_drafts_resources.services.records import RecordDraftServiceConfig
from invenio_records_resources.services.records.components import MetadataComponent
from invenio_records_resources.services.records.search import terms_filter

from invenio_records_marc21.indexer import Marc21RecordIndexer

from ..api import Marc21Draft, Marc21Record
from .components import AccessComponent, PIDComponent
from .permissions import Marc21RecordPermissionPolicy
from .schemas import Marc21RecordSchema, MetadataSchema


class Marc21RecordServiceConfig(RecordDraftServiceConfig):
    """Marc21 record service config."""

    # Record class
    record_cls = Marc21Record
    # Draft class
    draft_cls = Marc21Draft
    indexer_cls = Marc21RecordIndexer
    schema = Marc21RecordSchema
    # TODO: ussing from invenio-permissions
    permission_policy_cls = Marc21RecordPermissionPolicy

    search_facets_options = dict(
        aggs={},
        post_filters={
            "access_right": terms_filter("access.access_right"),
        },
    )

    components = [
        MetadataComponent,
        AccessComponent,
        PIDComponent,
    ]
