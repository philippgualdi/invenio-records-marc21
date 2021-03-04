# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 Graz University of Technology.
#
# invenio-records-lom is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Circulation PID providers."""

from invenio_pidstore.models import PIDStatus
from invenio_pidstore.providers.recordid_v2 import RecordIdProviderV2


class MarcIdProvider(RecordIdProviderV2):
    """Marc identifier provider.

    This PID provider requires a marc21 record to be passed, and relies
    on the marc21 record having an 'id' key and a type defined.
    """

    @classmethod
    def create(cls, object_type=None, object_uuid=None, record=None, **kwargs):
        """Create a new marc21 record identifier.

        Relies on the a marc21 record being

        Note: if the object_type and object_uuid values are passed, then the
        PID status will be automatically setted to
        :attr:`invenio_pidstore.models.PIDStatus.NEW`.

        For more information about parameters,
        see :meth:`invenio_pidstore.providers.base.BaseProvider.create`.

        :param object_type: The object type. (Default: None.)
        :param object_uuid: The object identifier. (Default: None).
        :param record: A marc21 record.
        :param kwargs: Addtional options
        :returns: A :class:`MarcIdProvider` instance.
        """
        # assert record is not None, "Missing or invalid 'record'."
        # assert "id" in record and isinstance(
        #    record["id"], str
        # ), "Missing 'id' key in record."

        # Retrieve pid type from type.
        pid_type = "marcid"
        # Retrieve pid type from type.
        if "id" in record:
            pid_value = record["id"]

        # You must assign immediately.
        assert object_uuid
        assert object_type

        return super().create(
            pid_type=pid_type,
            object_type=object_type,
            object_uuid=object_uuid,
            status=PIDStatus.NEW,
        )
