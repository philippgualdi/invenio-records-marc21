# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2024 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Marc21 Review service."""

from .community_inclusion import Marc21CommunityInclusion
from .community_submission import Marc21CommunitySubmission

__all__ = ("Marc21CommunityInclusion", "Marc21CommunitySubmission",)
