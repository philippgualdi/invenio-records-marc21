# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 Graz University of Technology.
#
# invenio-records-lom is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Indexer for Marc21."""

from invenio_indexer.api import RecordIndexer

from .api import Marc21Record


class Marc21RecordIndexer(RecordIndexer):
    """Marc21 indexer."""

    record_cls = Marc21Record
