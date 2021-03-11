# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Helper proxy to the state object."""

from flask import current_app
from werkzeug.local import LocalProxy

current_records_marc21 = LocalProxy(
    lambda: current_app.extensions["invenio-records-marc21"]
)
"""Helper proxy to get the current records marc21 extension."""
