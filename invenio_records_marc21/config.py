# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Default configuration."""

from __future__ import absolute_import, print_function

from invenio_records_rest.query import es_search_factory
from invenio_records_rest.utils import allow_all, check_elasticsearch

MARC21_REST_ENDPOINTS = {
    "marcid": dict(
        pid_type="marcid",
        pid_minter="marcid",
        pid_fetcher="marcid",
        default_endpoint_prefix=True,
        record_class="invenio_records_marc21.api:Marc21RecordBase",
        search_class="invenio_search.RecordsSearch",
        search_index=None,
        search_type=None,
        indexer_class="invenio_records_marc21.indexer:Marc21RecordIndexer",
        record_serializers={
            "application/json": (
                "invenio_records_marc21.serializers" ":json_v1_response"
            ),
        },
        search_serializers={
            "application/json": (
                "invenio_records_marc21.serializers" ":json_v1_search"
            ),
        },
        record_loaders={
            "application/json": ("invenio_records_marc21.loaders" ":json_v1"),
        },
        list_route="/marc/",
        item_route="/marc/<pid(marcid):pid_value>",
        default_media_type="application/json",
        max_result_window=10000,
        error_handlers=dict(),
        # TODO: Redefine these permissions to cover your auth needs
        create_permission_factory_imp=allow_all,
        read_permission_factory_imp=check_elasticsearch,
        update_permission_factory_imp=allow_all,
        delete_permission_factory_imp=allow_all,
    ),
}
"""REST API for invenio-records-marc21."""

MARC21_UI_ENDPOINTS = {
    "marcid": {
        "pid_type": "marcid",
        "route": "/marc/<pid_value>",
        "template": "invenio_records_marc21/record.html",
    },
}
"""Records UI for invenio-records-marc21."""

# SEARCH_UI_JSTEMPLATE_RESULTS = "templates/invenio_records_marc21/results.html"
"""Result list template."""

# PIDSTORE_RECID_FIELD = "marcid"

INVENIO_RECORDS_MARC21_ENDPOINTS_ENABLED = True
"""Enable/disable automatic endpoint registration."""
