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
from flask_principal import Identity, Need, UserNeed
from invenio_access import any_user
from invenio_app.factory import create_api
from invenio_vocabularies.records.models import VocabularyType
from invenio_vocabularies.services.service import VocabulariesService

from invenio_records_marc21.api import Draft
from invenio_records_marc21.services import Marc21RecordService, Metadata
from invenio_records_marc21.vocabularies import Vocabularies


@pytest.fixture(scope="module")
def create_app(instance_path):
    """Application factory fixture."""
    return create_api


@pytest.fixture(scope="function")
def vocabulary_clear(app):
    """Clears the Vocabulary singleton and pushes an application context.

    NOTE: app fixture pushes an application context
    """
    Vocabularies.clear()


@pytest.fixture()
def identity_simple():
    """Simple identity fixture."""
    i = Identity(1)
    i.provides.add(any_user)
    return i


@pytest.fixture()
def service(appctx):
    """Service instance."""
    return Marc21RecordService()


@pytest.fixture()
def example_record(app, db):
    """Example record."""
    record = Draft.create({}, metadata={"title": "Test"})
    db.session.commit()
    return record


@pytest.fixture()
def metadata():
    """Input data (as coming from the view layer)."""
    metadata = Metadata()
    metadata.xml = "<record><datafield tag='245' ind1='1' ind2='0'>\
            <subfield code='a'>laborum sunt ut nulla</subfield>\
    </datafield></record>"
    return metadata


@pytest.fixture()
def metadata2():
    """Input data (as coming from the view layer)."""
    metadata = Metadata()
    metadata.xml = "<record>\
    <datafield tag='245' ind1='1' ind2='0'>\
        <subfield code='a'>nulla sunt laborum</subfield>\
    </datafield></record>"
    return metadata
