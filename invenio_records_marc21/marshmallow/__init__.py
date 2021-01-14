# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Schemas for marshmallow."""

from __future__ import absolute_import, print_function

from .json import Marc21MetadataSchemaV1, Marc21RecordSchemaV1

__all__ = (
    "Marc21MetadataSchemaV1",
    "Marc21RecordSchemaV1",
)
