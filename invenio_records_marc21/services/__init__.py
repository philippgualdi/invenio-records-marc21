# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


"""High-level API for wokring with Marc21 records, pids and search."""

from .permissions import Marc21RecordPermissionPolicy
from .services import Marc21DataType, Marc21RecordService, Marc21RecordServiceConfig

__all__ = (
    "Marc21DataType",
    "Marc21RecordService",
    "Marc21RecordServiceConfig",
    "Marc21RecordPermissionPolicy",
)
