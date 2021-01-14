# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""JSON Schemas."""

from __future__ import absolute_import, print_function

from invenio_records_rest.schemas import Nested, StrictKeysMixin
from invenio_records_rest.schemas.fields import (
    DateString,
    PersistentIdentifier,
    SanitizedUnicode,
)
from marshmallow import fields, missing, validate


class Marc21MetadataSchemaV1(StrictKeysMixin):
    """Schema for the Marc21 metadata."""

    id = PersistentIdentifier()
    record = SanitizedUnicode(required=True)


class Marc21RecordSchemaV1(StrictKeysMixin):
    """Marc21 Record schema."""

    metadata = fields.Nested(Marc21MetadataSchemaV1)
    created = fields.Str(dump_only=True)
    revision = fields.Integer(dump_only=True)
    updated = fields.Str(dump_only=True)
    links = fields.Dict(dump_only=True)
    id = PersistentIdentifier()
