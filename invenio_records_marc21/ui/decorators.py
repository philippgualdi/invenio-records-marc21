# -*- coding: utf-8 -*-
#
# Copyright (C) 2019-2021 CERN.
# Copyright (C) 2019-2021 Northwestern University.
# Copyright (C)      2021 TU Wien.
# Copyright (C)      2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Routes for record-related pages provided by Invenio-Records-Marc21."""

from functools import wraps

from flask import g
from invenio_records_resources.services.errors import PermissionDeniedError

from ..proxies import current_records_marc21


def links_config():
    """Get the record links config."""
    return current_records_marc21.records_resource.config.links_config


def draft_links_config():
    """Get the drafts links config."""
    return current_records_marc21.records_resource.config.draft_links_config


def service():
    """Get the record service."""
    return current_records_marc21.records_service


def pass_record(f):
    """Decorate a view to pass a record using the record service."""

    @wraps(f)
    def view(**kwargs):
        pid_value = kwargs.get("pid_value")
        record = service().read(
            id_=pid_value, identity=g.identity, links_config=links_config()
        )
        kwargs["record"] = record
        return f(**kwargs)

    return view


def pass_draft(f):
    """Decorator to retrieve the draft using the record service."""

    @wraps(f)
    def view(**kwargs):
        pid_value = kwargs.get("pid_value")
        draft = service().read_draft(
            id_=pid_value, identity=g.identity, links_config=draft_links_config()
        )
        # TODO: Remove - all this should happen in service
        # Dereference relations (languages, licenses, etc.)
        draft._record.relations.dereference()
        kwargs["draft"] = draft
        return f(**kwargs)

    return view


def user_permissions(actions=[]):
    """Decorate a view to pass user's permissions for the provided actions.

    :param actions: The action list to check permissions against.
    """

    def _wrapper_func(f):
        @wraps(f)
        def view(**kwargs):
            action_args = {}
            if "record" in kwargs:
                # Permissions deal with record data objects, not result items
                action_args["record"] = kwargs["record"]._record
            elif "draft" in kwargs:
                # Permissions deal with record data objects, not result items
                # TODO: We need a way in the service to pass a result item
                # and ask for the permissions (to avoid accessing internal obj)
                action_args["record"] = kwargs["draft"]._record
            permissions = {}
            for action in actions:
                action_can = (
                    service()
                    .permission_policy(action, **action_args)
                    .allows(g.identity)
                )
                permissions[f"can_{action}"] = action_can
            kwargs["permissions"] = permissions
            return f(**kwargs)

        return view

    return _wrapper_func
