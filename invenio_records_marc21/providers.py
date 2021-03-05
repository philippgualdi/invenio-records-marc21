# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 Graz University of Technology.
#
# invenio-records-lom is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Marc PID providers."""

from invenio_pidstore.models import PIDStatus
from invenio_pidstore.providers.recordid_v2 import RecordIdProviderV2
from invenio_pidstore.resolver import Resolver


class MarcResolver(Resolver):
    def __init__(
        self, pid_type="marcid", object_type="rec", getter=None, registered_only=False
    ):
        """Initialize resolver.

        :param pid_type: Persistent identifier type.
        :param object_type: Object type.
        :param getter: Callable that will take an object id for the given
            object type and retrieve the internal object.
        """
        self.pid_type = pid_type
        self.object_type = object_type
        self.object_getter = getter
        self.registered_only = registered_only


class MarcRecordProvider(RecordIdProviderV2):
    """Marc records identifier provider.

    This PID provider requires a marc21 record to be passed, and relies
    on the marc21 record having an 'id' key and a type defined.
    """

    pid_type = "marcid"


class MarcDraftProvider(MarcRecordProvider):
    """Marc draft records identifier provider.

    This PID provider requires a marc21 draft record to be passed, and relies
    on the marc21 record having an 'id' key and a type defined.
    """

    default_status_with_obj = PIDStatus.NEW
