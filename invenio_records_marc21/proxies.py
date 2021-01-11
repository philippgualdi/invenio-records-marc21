# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Graz University of Technology.
#
# invenio-records-marc21 is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Proxy definitions."""

from __future__ import absolute_import, print_function

from flask import current_app
from werkzeug.local import LocalProxy

current_marc21record = LocalProxy(
    lambda: current_app.extensions["invenio-records-marc21"]
)
"""Proxy to the extension."""

Marc21 = LocalProxy(lambda: current_app.extensions["invenio-records-marc21"].marc21_cls)
"""Proxy for current marc21 class."""
