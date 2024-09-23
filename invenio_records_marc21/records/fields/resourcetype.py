# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2023 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Resource type field."""

from enum import Enum


class ResourceTypeEnum(Enum):
    """Enum defining resource type."""

    HSMASTER = "HS-MASTER"

    HSDISS = "HS-DISS"

    CATALOGUE = "CATALOGUE"

    CHAPTER = "CHAPTER"
