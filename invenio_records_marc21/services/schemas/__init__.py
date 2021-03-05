# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Marc21 record schemas."""

from invenio_records_resources.services.records.schema import RecordSchema
from marshmallow import EXCLUDE, INCLUDE, Schema, fields, missing, post_dump

from .access import AccessSchema
from .metadata import MetadataSchema
from .pids import PIDSchema


class AttributeAccessorFieldMixin:
    """Marshmallow field mixin for attribute-based serialization."""

    def get_value(self, obj, attr, accessor=None, default=missing):
        """Return the value for a given key from an object attribute."""
        attribute = getattr(self, "attribute", None)
        check_key = attr if attribute is None else attribute
        return getattr(obj, check_key, default)


class NestedAttribute(fields.Nested, AttributeAccessorFieldMixin):
    """Nested object attribute field."""


class Marc21RecordSchema(RecordSchema):
    """Record schema."""

    class Meta:
        """Meta class."""

        unknown = EXCLUDE

    id = fields.Str()
    # pid
    conceptid = fields.Str(dump_only=True)
    # conceptpid
    pids = fields.List(NestedAttribute(PIDSchema))
    metadata = NestedAttribute(MetadataSchema)
    access = NestedAttribute(AccessSchema)
    # files = NestedAttribute(FilesSchema, dump_only=True)
    created = fields.Str(dump_only=True)
    updated = fields.Str(dump_only=True)
    revision = fields.Integer(dump_only=True)
    status = fields.Str(dump_only=True)

    published = fields.Boolean(attribute="is_published", dump_only=True)

    @post_dump
    def default_nested(self, data, many, **kwargs):
        """Serialize metadata as empty dict for partial drafts.

        Cannot use marshmallow for Nested fields due to issue:
        https://github.com/marshmallow-code/marshmallow/issues/1566
        https://github.com/marshmallow-code/marshmallow/issues/41
        and more.
        """
        if not data.get("metadata"):
            data["metadata"] = {}

        return data


__all__ = ("Marc21RecordSchema",)
