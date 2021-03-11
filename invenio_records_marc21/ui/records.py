# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


"""Routes for record-related pages provided by Invenio-App-RDM."""

from flask import render_template

from ..resources.serializers.ui import UIJSONSerializer
from .decorators import pass_record, user_permissions


#
# Views
#
@pass_record
@user_permissions(actions=["update_draft"])
def record_detail(record=None, files=None, pid_value=None, permissions=None):
    """Record detail page (aka landing page)."""
    files_dict = None if files is None else files.to_dict()
    return render_template(
        "invenio_records_marc21/record.html",
        record=UIJSONSerializer().serialize_object_to_dict(record.to_dict()),
        pid=pid_value,
        files=files_dict,
        permissions=permissions,
    )


def marc21_index(permissions=None):
    """Record detail page (aka landing page)."""
    return render_template(
        "invenio_records_marc21/index.html",
        permissions=permissions,
    )
