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
    assert draft_dict["errors"][0]["field"] == "metadata.title"


def test_read_draft(app, service, identity_simple, metadata):
    # Needs `app` context because of invenio_access/permissions.py#166
    draft = service.create(identity_simple, metadata=metadata)
    assert draft.id

    draft_2 = service.read_draft(draft.id, identity_simple)
    assert draft.id == draft_2.id


def test_update_draft(app, service, identity_simple, metadata):
    # Needs `app` context because of invenio_access/permissions.py#166
    draft = service.create(identity_simple, metadata=metadata)
    assert draft.id

    orig_metadata = metadata.xml
    edited_metadata = "<record>\
    <datafield tag='245' ind1='1' ind2='0'>\
        <subfield code='a'>nulla sunt laborum</subfield>\
    </datafield></record>"
    metadata.xml = edited_metadata

    # Update draft content
    update_draft = service.update_draft(draft.id, identity_simple, metadata=metadata)
    assert update_draft["metadata"] == edited_metadata
    assert draft.id == update_draft.id

    # Check the updates where saved
    update_draft = service.read_draft(draft.id, identity_simple)
    assert draft.id == update_draft.id
    assert update_draft["metadata"] == edited_metadata


def test_update_draft_invalid_field(app, service, identity_simple, metadata):
    """Update with invalid field reports rather than raises errors."""
    # Needs `app` context because of invenio_access/permissions.py#166
    draft = service.create(identity_simple, metadata=metadata)
    orig_title = metadata["metadata"]["title"]
    edited_title = 100
    metadata["metadata"]["title"] = edited_title

    updated_draft = service.update_draft(draft.id, identity_simple, metadata)
    updated_draft_dict = updated_draft.to_dict()

    assert draft.id == updated_draft.id
    assert updated_draft["metadata"]["title"] == orig_title
    assert updated_draft_dict["errors"][0]["field"] == "metadata.title"


def test_delete_draft(app, service, identity_simple, metadata):
    # Needs `app` context because of invenio_access/permissions.py#166
    draft = service.create(identity_simple, metadata)
    assert draft.id

    success = service.delete_draft(draft.id, identity_simple)
    assert success

    # Check draft deletion
    with pytest.raises(NoResultFound):
        # NOTE: Draft and Record have the same `id`
        delete_draft = service.read_draft(draft.id, identity_simple)


def _create_and_publish(service, metadata, identity_simple):
    """Creates a draft and publishes it."""
    # Cannot create with record service due to the lack of versioning
    draft = service.create(identity_simple, metadata)

    record = service.publish(draft.id, identity_simple)

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

    for key, value in metadata.items():
        assert record[key] == value

    # Check draft deletion
    with pytest.raises(NoResultFound):
        # NOTE: Draft and Record have the same `id`
        draft = service.read_draft(record.id, identity_simple)

    # Test record exists
    record = service.read(record.id, identity_simple)

    assert record.id
    assert record._record.pid.status == PIDStatus.REGISTERED
    assert record._record.conceptpid.status == PIDStatus.REGISTERED

    for key, value in metadata.items():
        assert record[key] == value


def test_fail_to_publish_invalid_draft(app, service, identity_simple):
    """Publishing an incomplete draft should fail.

    Note that the publish action requires a draft to be created first.
    """
    # Needs `app` context because of invenio_access/permissions.py#166
    input_data = {"metadata": {}}
    draft = service.create(identity_simple, input_data)

    with pytest.raises(ValidationError) as e:
        record = service.publish(draft.id, identity_simple)

    exception = e.value
    assert "metadata" not in exception.valid_data

    # Draft still there
    draft = service.read_draft(draft.id, identity_simple)
    assert draft
    assert draft._record.pid.status == PIDStatus.NEW
    assert draft._record.conceptpid.status == PIDStatus.NEW

    # Test no published record exists
    with pytest.raises(PIDUnregistered) as e:
        record = service.read(draft.id, identity_simple)


#
# Flow tests (Note that operations are tested above
# therefore these tests do not assert their output)
#


def test_create_publish_new_revision(app, service, identity_simple, input_data):
    """Test creating a new revision of a record.

    This tests the `edit` service method.
    """
    # Needs `app` context because of invenio_access/permissions.py#166
    record = _create_and_publish(service, input_data, identity_simple)
    recid = record.id

    # Create new draft of said record
    draft = service.edit(recid, identity_simple)
    assert draft.id == recid
    assert draft._record.fork_version_id == record._record.revision_id
    # create, soft-delete, undelete, update
    assert draft._record.revision_id == 4

    # Update the content
    orig_title = input_data["metadata"]["title"]
    edited_title = "Edited title"
    input_data["metadata"]["title"] = edited_title

    update_draft = service.update_draft(draft.id, identity_simple, input_data)

    # Check the actual record was not modified
    record = service.read(recid, identity_simple)
    assert record["metadata"]["title"] == orig_title

    # Publish it to check the increment in version_id
    record = service.publish(recid, identity_simple)

    assert record.id == recid
    assert record._record.revision_id == 2
    assert record["metadata"]["title"] == edited_title

    # Check it was actually edited
    record = service.read(recid, identity_simple)
    assert record["metadata"]["title"] == edited_title


def test_mutiple_edit(app, service, identity_simple, input_data):
    """Test the revision_id when editing record multiple times..

    This tests the `edit` service method.
    """
    # Needs `app` context because of invenio_access/permissions.py#166
    record = _create_and_publish(service, input_data, identity_simple)
    recid = record.id

    # Create new draft of said record
    draft = service.edit(recid, identity_simple)
    assert draft.id == recid
    assert draft._record.fork_version_id == record._record.revision_id
    assert draft._record.revision_id == 4

    draft = service.edit(recid, identity_simple)
    assert draft.id == recid
    assert draft._record.fork_version_id == record._record.revision_id
    assert draft._record.revision_id == 4

    # Publish it to check the increment in version_id
    record = service.publish(recid, identity_simple)

    draft = service.edit(recid, identity_simple)
    assert draft.id == recid
    assert draft._record.fork_version_id == record._record.revision_id
    assert draft._record.revision_id == 7  # soft-delete, undelete, update


def test_create_publish_new_version(app, service, identity_simple, input_data):
    """Test creating a new revision of a record.

    This tests the `new_version` service method.
    """
    # Needs `app` context because of invenio_access/permissions.py#166
    record = _create_and_publish(service, input_data, identity_simple)
    recid = record.id

    # Create new version
    draft = service.new_version(recid, identity_simple)

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
