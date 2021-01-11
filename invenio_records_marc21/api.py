# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Graz University of Technology.
#
# invenio-records-marc21 is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Marc21 Api."""

from __future__ import absolute_import, print_function

from flask import current_app
from invenio_db import db
from invenio_jsonschemas import current_jsonschemas
from invenio_pidstore.models import PersistentIdentifier
from invenio_pidstore.resolver import Resolver
from invenio_records.api import Record
from invenio_records.models import RecordMetadata
from werkzeug.local import LocalProxy

from .signals import marc21record_created

# TODO: uncomment to use the model for db manipulation
# from invenio_records_marc21.models import Marc21Metadata


# TODO: Move somewhere appropriate (`invenio-records-pidstore`)
class PIDRecordMixin:
    """Persistent identifier mixin for records."""

    object_type = None
    pid_type = None

    @property
    def pid(self):
        """Return primary persistent identifier of the record."""
        return PersistentIdentifier.query.filter_by(
            object_uuid=self.id, object_type=self.object_type, pid_type=self.pid_type
        ).one()

    @classmethod
    def resolve(cls, pid_value):
        """Resolve a PID value and return the PID and record."""
        return Resolver(
            pid_type=cls.pid_type, object_type=cls.object_type, getter=cls.get_record
        ).resolve(pid_value)


class Marc21RecordBase(Record, PIDRecordMixin):
    """Define API for Marc21 creation and manipulation."""

    object_type = "marc21"
    pid_type = "marcid"

    model_cls = RecordMetadata
    schema = LocalProxy(
        lambda: current_jsonschemas.path_to_url(
            current_app.config.get("MARC21_SCHEMA", "marc21/marc21-v1.0.0.json")
        )
    )

    @classmethod
    def create(cls, data, id_=None, **kwargs):
        """Create a new Marc21 instance and store it in the database."""
        with db.session.begin_nested():
            if "schema" in data:
                data["$schema"] = current_jsonschemas.path_to_url(data["schema"])
                data.pop("schema")
            else:
                data["$schema"] = str(cls.schema)
            marc21 = cls(data)
            marc21.validate(**kwargs)
            marc21.model = cls.model_cls(id=id_, json=marc21)
            db.session.add(marc21.model)
            marc21record_created.send(marc21)
        return marc21

    def clear(self):
        """Clear but preserve the schema field."""
        schema = self["$schema"]
        # TODO: since this is a "system" field, in the future it should be
        # auto-preserved
        collections = self.get("_collections")
        super(Marc21RecordBase, self).clear()
        self["$schema"] = schema
        if collections:
            self["_collections"] = collections

    def delete(self, force=False):
        """Delete a Marc21."""
        with db.session.begin_nested():
            if force:
                db.session.delete(self.model)
            else:
                self.model.delete()
        return self
