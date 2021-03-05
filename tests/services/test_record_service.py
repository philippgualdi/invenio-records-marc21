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
from dojson.contrib.marc21.utils import create_record
from dojson.contrib.to_marc21 import to_marc21
from invenio_pidstore.errors import (
    PIDDeletedError,
    PIDDoesNotExistError,
    PIDUnregistered,
)
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
    with pytest.raises(PIDDoesNotExistError):
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


def _test_metadata(metadata, metadata2):
    assert metadata.keys() == metadata2.keys()
    for key in metadata.keys():
        assert metadata[key] == metadata2[key]


def test_update_draft(app, service, identity_simple, metadata, metadata2):
    # Needs `app` context because of invenio_access/permissions.py#166
    draft = service.create(identity=identity_simple, metadata=metadata)
    assert draft.id

    # Update draft content
    update_draft = service.update_draft(
        draft.id, identity=identity_simple, metadata=metadata2
    )

    assert draft.id == update_draft.id
    _test_metadata(
        to_marc21.do(update_draft["metadata"]["json"]), create_record(metadata.xml)
    )
    # Check the updates where savedif "json" in data:

    read_draft = service.read_draft(id_=draft.id, identity=identity_simple)

    assert draft.id == update_draft.id
    _test_metadata(
        to_marc21.do(update_draft["metadata"]["json"]),
        to_marc21.do(read_draft["metadata"]["json"]),
    )


def test_mutiple_edit(app, service, identity_simple, metadata):
    """Test the revision_id when editing record multiple times..

    This tests the `edit` service method.
    """
    # Needs `app` context because of invenio_access/permissions.py#166
    record = _create_and_publish(service, metadata, identity_simple)
    marcid = record.id

    # Create new draft of said record
    draft = service.edit(marcid, identity_simple)
    assert draft.id == marcid
    assert draft._record.fork_version_id == record._record.revision_id
    assert draft._record.revision_id == 4

    draft = service.edit(marcid, identity_simple)
    assert draft.id == marcid
    assert draft._record.fork_version_id == record._record.revision_id
    assert draft._record.revision_id == 4

    # Publish it to check the increment in version_id
    record = service.publish(marcid, identity_simple)

    draft = service.edit(marcid, identity_simple)
    assert draft.id == marcid
    assert draft._record.fork_version_id == record._record.revision_id
    assert draft._record.revision_id == 7  # soft-delete, undelete, update


def test_create_publish_new_version(app, service, identity_simple, metadata):
    """Test creating a new revision of a record.

    This tests the `new_version` service method.
    """
    # Needs `app` context because of invenio_access/permissions.py#166
    record = _create_and_publish(service, metadata, identity_simple)
    marcid = record.id

    # Create new version
    draft = service.new_version(marcid, identity_simple)

    assert draft._record.revision_id == 1
    assert draft["conceptid"] == record["conceptid"]
    assert draft["id"] != record["id"]
    assert draft._record.pid.status == PIDStatus.NEW
    assert draft._record.conceptpid.status == PIDStatus.REGISTERED

    # Publish it
    record_2 = service.publish(draft.id, identity_simple)

    assert record_2.id
    assert record_2._record.pid.status == PIDStatus.REGISTERED
    assert record_2._record.conceptpid.status == PIDStatus.REGISTERED
    assert record_2._record.revision_id == 1
    assert record_2["conceptid"] == record["conceptid"]
    assert record_2["id"] != record["id"]
