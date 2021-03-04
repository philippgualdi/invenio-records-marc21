# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


"""Module tests."""
from datetime import date, timedelta

import pytest
from flask_principal import Identity
from invenio_access import any_user

from invenio_records_marc21.models import DraftMetadata, RecordMetadata
from invenio_records_marc21.services import Marc21RecordService


def _assert_fields_exists(fields, data):
    for key in fields:
        assert key in data


def _assert_fields(fields, values, expected):
    for key in fields:
        assert values[key] == expected[key]


@pytest.fixture()
def marc21():
    """marc21 record."""
    return {"metadata": {"xml": "<record></record>"}}


def test_create_with_service(app, marc21, identity_simple):

    service = Marc21RecordService()

    draft = service.create(data=marc21, identity=identity_simple, access=None)

    root_fields = [
        "id",
        "conceptid",
        "created",
        "updated",
        "metadata",
        "access",
    ]
    expected = {"metadata": {}}
    _assert_fields_exists(root_fields, draft.data)
    _assert_fields(["metadata"], draft.data, expected)

    record = service.publish(id_=draft.id, identity=identity_simple)

    assert record
    _assert_fields_exists(root_fields, record.data)
    _assert_fields(["metadata"], record.data, expected)


@pytest.fixture()
def empty_data():
    """marc21 record."""
    return {"metadata": {"xml": "<record></record>"}}


@pytest.mark.parametrize(
    "access",
    [
        {
            "input": {
                "access_right": "open",
            },
            "expect": {
                "access": {
                    "metadata": False,
                    "owned_by": [{"user": 1}],
                    "access_right": "open",
                },
            },
        },
        {
            "input": {
                "access_right": "closed",
            },
            "expect": {
                "access": {
                    "metadata": False,
                    "owned_by": [{"user": 1}],
                    "access_right": "closed",
                },
            },
        },
        {
            "input": {
                "access_right": "embargoed",
                "embargo_date": (date.today() + timedelta(days=2)).strftime("%Y-%m-%d"),
            },
            "expect": {
                "access": {
                    "metadata": False,
                    "owned_by": [{"user": 1}],
                    "access_right": "embargoed",
                    "embargo_date": (date.today() + timedelta(days=2)).strftime(
                        "%Y-%m-%d"
                    ),
                },
            },
        },
        {
            "input": {
                "access_right": "restricted",
                "embargo_date": (date.today() + timedelta(days=3)).strftime("%Y-%m-%d"),
            },
            "expect": {
                "access": {
                    "metadata": False,
                    "owned_by": [{"user": 1}],
                    "access_right": "restricted",
                    "embargo_date": (date.today() + timedelta(days=3)).strftime(
                        "%Y-%m-%d"
                    ),
                },
            },
        },
    ],
)
def test_create_with_access(app, empty_data, identity_simple, access):

    service = Marc21RecordService()
    draft = service.create(
        data=empty_data, identity=identity_simple, access=access["input"]
    )
    record = service.publish(id_=draft.id, identity=identity_simple)

    _assert_fields(
        ["access"],
        record.data,
        access["expect"],
    )
