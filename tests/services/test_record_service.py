# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Service tests.

Test to add:
- Read a tombstone page
- Read with missing permissions
- Read with missing pid
"""

import time

import pytest
from invenio_pidstore.errors import PIDDeletedError, PIDUnregistered
from invenio_pidstore.models import PIDStatus
from invenio_search import current_search, current_search_client
from marshmallow.exceptions import ValidationError
from sqlalchemy.orm.exc import NoResultFound

from invenio_records_marc21.services import Metadata

#
# Operations tests
#


def test_create_draft(app, service, identity_simple, metadata):
    """Test draft creation of a non-existing record."""
    # Needs `app` context because of invenio_access/permissions.py#166
    draft = service.create(identity_simple, metadata=metadata)
    draft_dict = draft.to_dict()

    assert draft.id
    assert draft._record.revision_id == 1

    # Check for pid and parent pid
    assert draft["id"]
    assert draft["conceptid"]
    assert draft._record.pid.status == PIDStatus.NEW
    assert draft._record.conceptpid.status == PIDStatus.NEW


def test_create_empty_draft(app, service, identity_simple):
    """Test an empty draft can be created.

    Errors (missing required fields) are reported, but don't prevent creation.
    """
    # Needs `app` context because of invenio_access/permissions.py#166
    input_data = {"metadata": {}}

    draft = service.create(identity_simple, input_data)
    draft_dict = draft.to_dict()

    assert draft["id"]
    assert draft["conceptid"]
    assert draft._record.pid.status == PIDStatus.NEW
    assert draft._record.conceptpid.status == PIDStatus.NEW


def test_read_draft(app, service, identity_simple, metadata):
    # Needs `app` context because of invenio_access/permissions.py#166
    draft = service.create(identity_simple, metadata=metadata)
    assert draft.id

    draft_2 = service.read_draft(draft.id, identity_simple)
    assert draft.id == draft_2.id


def test_delete_draft(app, service, identity_simple, metadata):
    # Needs `app` context because of invenio_access/permissions.py#166
    draft = service.create(identity=identity_simple, metadata=metadata)
    assert draft.id

    success = service.delete_draft(draft.id, identity_simple)
    assert success

    # Check draft deletion
    with pytest.raises(NoResultFound):
        # NOTE: Draft and Record have the same `id`
        delete_draft = service.read_draft(draft.id, identity=identity_simple)


def _create_and_publish(service, metadata, identity_simple):
    """Creates a draft and publishes it."""
    # Cannot create with record service due to the lack of versioning
    draft = service.create(identity=identity_simple, metadata=metadata)

    record = service.publish(draft.id, identity=identity_simple)

    assert record.id == draft.id
    assert record._record.revision_id == 1

    return record


def test_publish_draft(app, service, identity_simple, metadata):
    """Test draft publishing of a non-existing record.

    Note that the publish action requires a draft to be created first.
    """
    # Needs `app` context because of invenio_access/permissions.py#166
    record = _create_and_publish(service, metadata, identity_simple)
    assert record._record.pid.status == PIDStatus.REGISTERED
    assert record._record.conceptpid.status == PIDStatus.REGISTERED

    # Check draft deletion
    with pytest.raises(NoResultFound):
        # NOTE: Draft and Record have the same `id`
        draft = service.read_draft(id_=record.id, identity=identity_simple)

    # Test record exists
    record = service.read(id_=record.id, identity=identity_simple)

    assert record.id
    assert record._record.pid.status == PIDStatus.REGISTERED
    assert record._record.conceptpid.status == PIDStatus.REGISTERED


def test_fail_to_publish_invalid_draft(app, service, identity_simple):
    """Publishing an incomplete draft should fail.

    Note that the publish action requires a draft to be created first.
    """
    # Needs `app` context because of invenio_access/permissions.py#166
    input_data = Metadata()
    draft = service.create(identity=identity_simple, metadata=input_data)

    with pytest.raises(ValidationError) as e:
        record = service.publish(id_=draft.id, identity=identity_simple)

    exception = e.value
    assert "metadata" not in exception.valid_data

    # Draft still there
    draft = service.read_draft(id_=draft.id, identity=identity_simple)
    assert draft
    assert draft._record.pid.status == PIDStatus.NEW
    assert draft._record.conceptpid.status == PIDStatus.NEW

    # Test no published record exists
    with pytest.raises(PIDUnregistered) as e:
        record = service.read(id_=draft.id, identity=identity_simple)
