# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2024 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Marc21 Community addition request."""

from invenio_rdm_records.requests import CommunityInclusion


#
# Request
#
class Marc21CommunityInclusion(CommunityInclusion):
    """Community inclusion request for adding a record to a community."""

    type_id = "marc21-community-inclusion"
    allowed_topic_ref_types = ["record"]

