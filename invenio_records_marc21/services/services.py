# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


"""Marc21 Record Service."""

from datetime import date
from enum import Enum

from invenio_drafts_resources.services.records import (
    RecordDraftService,
    RecordDraftServiceConfig,
)
from invenio_records_resources.services.records.components import MetadataComponent
from invenio_records_resources.services.records.search import terms_filter

from ..api import Marc21Draft, Marc21Record
from .components import AccessComponent
from .permissions import Marc21RecordPermissionPolicy
from .schemas import Marc21RecordSchema


class Marc21DataType(Enum):
    """Marc21 data types."""

    RECORD_FULL = 1
    RECORD_METADATA = 2


class Marc21RecordServiceConfig(RecordDraftServiceConfig):
    """Marc21 record service config."""

    # Record class
    record_cls = Marc21Record
    # Draft class
    draft_cls = Marc21Draft

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
    ]


class Marc21RecordService(RecordDraftService):
    """Marc21 record service."""

    config_name = "MARC21_RECORDS_SERVICE_CONFIG"
    default_config = Marc21RecordServiceConfig

    def create(
        self,
        identity,
        data,
        links_config=None,
        data_type=Marc21DataType.RECORD_FULL,
        access=None,
    ):
        """Create a draft record.

        :param identity: Identity of user creating the record.
        :param dict|string data: Input data according to the data schema or a marc21 string.
        :param links_config: Links configuration.
        :param enum data_type: Input data structure, RECORD_FULL assumes a dict and
             RECORD_METADATA assumse a xml string.
        :param dict access: provide access additional information
        """
        if data_type == Marc21DataType.RECORD_METADATA:
            data = {
                "metadata": {"record": data},
            }

        if "access" not in data:
            default_access = {
                "access": {
                    "metadata": False,
                    "owned_by": [identity.id],
                    "access_right": "open",
                    "embargo_date": date.today().strftime("%Y-%m-%d"),
                },
            }
            if access is not None:
                default_access["access"].update(access)
            data.update(default_access)
        return super().create(identity, data, links_config)
