# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Flask extension for Invenio-Records-Marc21."""

from __future__ import absolute_import, print_function

from werkzeug.utils import cached_property

from . import config


class InvenioRecordsMARC21(object):
    """Invenio-Records-Marc21 extension."""

    def __init__(self, app=None):
        """Extension initialization."""
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Flask application initialization."""
        self.init_config(app)
        app.extensions["invenio-records-marc21"] = self

    @cached_property
    def marc21_cls(self):
        """Base Marc21 API class."""
        from .api import Marc21RecordBase

        return type(
            "Marc21",
            (Marc21RecordBase,),
            {},
        )

    def init_config(self, app):
        """Initialize configuration.

        Override configuration variables with the values in this package.
        """
        with_endpoints = app.config.get(
            "INVENIO_RECORDS_MARC21_ENDPOINTS_ENABLED", True
        )
        for k in dir(config):
            if k.startswith("MARC21_"):
                if k == "MARC21_REST_ENDPOINTS":
                    app.config.setdefault("RECORDS_REST_ENDPOINTS", {})
                    app.config["RECORDS_REST_ENDPOINTS"].update(getattr(config, k))
                elif k == "MARC21_UI_ENDPOINTS":
                    app.config.setdefault("RECORDS_UI_ENDPOINTS", {})
                    app.config["RECORDS_UI_ENDPOINTS"].update(getattr(config, k))
                app.config.setdefault(k, getattr(config, k))
