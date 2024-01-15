# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2024 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Record communities service."""

from .config import Marc21RecordCommunitiesConfig
from .service import Marc21RecordCommunitiesService

__all__ = (
    "Marc21RecordCommunitiesConfig",
    "Marc21RecordCommunitiesService",
)
