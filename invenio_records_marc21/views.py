# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Marc21 converter"""

# TODO: This is an example file. Remove it if you do not need it, including
# the templates and static folders as well as the test case.

from flask import Blueprint, render_template
from flask_babelex import gettext as _

blueprint = Blueprint(
    "invenio_records_marc21",
    __name__,
    template_folder="templates",
    static_folder="static",
)


@blueprint.route("/")
def index():
    """Render a basic view."""
    return render_template(
        "invenio_records_marc21/index.html", module_name=_("Invenio-Records-Marc21")
    )
