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
