# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.


"""Pytest configuration.

See https://pytest-invenio.readthedocs.io/ for documentation on which test
fixtures are available.
"""

import pytest
from flask_principal import Identity
from invenio_access import any_user
from invenio_app.factory import create_api

from invenio_records_marc21.records import Marc21Draft
from invenio_records_marc21.services import (
    Marc21RecordService,
    Marc21RecordServiceConfig,
)
from invenio_records_marc21.services.record import Marc21Metadata


@pytest.fixture(scope="module")
def create_app(instance_path):
    """Application factory fixture."""
    return create_api


@pytest.fixture()
def identity_simple():
    """Simple identity fixture."""
    i = Identity(1)
    i.provides.add(any_user)
    return i


@pytest.fixture()
def service(appctx):
    """Service instance."""
    return Marc21RecordService(config=Marc21RecordServiceConfig())


@pytest.fixture()
def example_record(app, db):
    """Example record."""
    record = Marc21Draft.create({}, metadata={"title": "Test"})
    db.session.commit()
    return record


@pytest.fixture()
def metadata():
    """Input data (as coming from the view layer)."""
    metadata = Marc21Metadata()
    metadata.add_value(tag="245", ind1="1", ind2="0", value="laborum sunt ut nulla")
    return metadata


@pytest.fixture()
def metadata2():
    """Input data (as coming from the view layer)."""
    metadata = Marc21Metadata()
    metadata.add_value(tag="245", ind1="1", ind2="0", value="nulla sunt laborum")
    return metadata
