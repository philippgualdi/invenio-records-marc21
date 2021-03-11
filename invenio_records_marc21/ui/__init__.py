# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Records user interface."""

from flask import Blueprint
from invenio_pidstore.errors import PIDDeletedError, PIDDoesNotExistError
from invenio_records_resources.services.errors import PermissionDeniedError

from .errors import (
    not_found_error,
    record_permission_denied_error,
    record_tombstone_error,
)
from .filters import pid_url
from .records import marc21_index, record_detail


#
# Registration
#
def create_blueprint(app):
    """Register blueprint routes on app."""
    routes = app.config.get("MARC21_UI_ENDPOINTS")

    blueprint = Blueprint(
        "invenio_records_marc21",
        __name__,
        template_folder="../templates",
    )

    # Record URL rules
    blueprint.add_url_rule(
        routes["index"],
        view_func=marc21_index,
    )

    # Record URL rules
    blueprint.add_url_rule(
        routes["record_detail"],
        view_func=record_detail,
    )

    # Register error handlers
    blueprint.register_error_handler(PIDDeletedError, record_tombstone_error)
    blueprint.register_error_handler(PIDDoesNotExistError, not_found_error)
    blueprint.register_error_handler(KeyError, not_found_error)
    blueprint.register_error_handler(
        PermissionDeniedError, record_permission_denied_error
    )

    blueprint.add_app_template_filter(pid_url)

    return blueprint
