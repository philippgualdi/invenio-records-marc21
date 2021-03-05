# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


"""Marc21 Record Service."""

from invenio_drafts_resources.services.records import RecordDraftService
from invenio_records_resources.services.records.components import MetadataComponent

from ..api import Marc21Draft, Marc21Record
from .components import AccessComponent
from .config import Marc21RecordServiceConfig
from .permissions import Marc21RecordPermissionPolicy
from .schemas import Marc21RecordSchema, MetadataSchema


class Metadata:
    """Marc21 Metadata object."""

    _json = {}
    _xml = ""

    @property
    def json(self):
        """Metadata json getter method."""
        return self._json

    @json.setter
    def json(self, json: dict):
        """Metadata json setter method."""
        if not isinstance(json, dict):
            raise TypeError("json must be from type dict")
        self._json = json

    @property
    def xml(self):
        """Metadata xml getter method."""
        return self._xml

    @xml.setter
    def xml(self, xml: str):
        """Metadata xml setter method."""
        if not isinstance(xml, str):
            raise TypeError("xml must be from type str")
        self._xml = xml


class Marc21RecordService(RecordDraftService):
    """Marc21 record service."""

    config_name = "MARC21_RECORDS_SERVICE_CONFIG"
    default_config = Marc21RecordServiceConfig

    def _create_data(self, identity, data, metadata, access=None):
        """Create a data json.

        :param identity: Identity of user creating the record.
        :param Metadata metadata: Input data according to the metadata schema.
        :param dict access: provide access additional information
        :return data: marc21 record data
        """
        if data is None:
            data = {"metadata": {"xml": metadata.xml, "json": metadata.json}}
        if "access" not in data:
            default_access = {
                "access": {
                    "metadata": False,
                    "owned_by": [{"user": identity.id}],
                    "access_right": "open",
                },
            }
            if access is not None:
                default_access["access"].update(access)
            data.update(default_access)
        return data

    def create(
        self, identity, data=None, metadata=Metadata(), links_config=None, access=None
    ):
        """Create a draft record.

        :param identity: Identity of user creating the record.
        :param dict data: Input data according to the data schema.
        :param Metadata metadata: Input data according to the metadata schema.
        :param links_config: Links configuration.
        :param dict access: provide access additional information
        """
        data = self._create_data(identity, data, metadata, access)
        return super().create(identity, data, links_config)

    def update_draft(
        self,
        id_,
        identity,
        data=None,
        metadata=Metadata(),
        links_config=None,
        revision_id=None,
        access=None,
    ):
        """Update a draft record.

        :param identity: Identity of user creating the record.
        :param dict data: Input data according to the data schema.
        :param Metadata metadata: Input data according to the metadata schema.
        :param links_config: Links configuration.
        :param dict access: provide access additional information
        """
        data = self._create_data(identity, data, metadata, access)
        return super().update_draft(id_, identity, data, links_config, revision_id)
