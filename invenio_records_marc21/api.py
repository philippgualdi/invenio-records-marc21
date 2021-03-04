# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Graz University of Technology.
#
# invenio-records-marc21 is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Marc21 Api."""

from __future__ import absolute_import, print_function

from invenio_drafts_resources.records import Draft, Record
from invenio_pidstore.resolver import Resolver
from invenio_records.systemfields import RelationsField
from invenio_records_resources.records.systemfields import IndexField, PIDField

from . import models
from .providers import MarcIdProvider
from .systemfields import Marc21PIDFieldContext


class Marc21Draft(Draft):
    """Marc21 draft API."""

    model_cls = models.DraftMetadata

    index = IndexField(
        "marc21records-drafts-marc21-v1.0.0", search_alias="marc21records-marc21"
    )

    pid = PIDField(
        key="id",
        pid_type="marcid",
        object_type="rec",
        provider=MarcIdProvider,
        context_cls=Marc21PIDFieldContext,
        resolver_cls=Resolver,
    )

    conceptpid = PIDField(
        key="conceptid",
        pid_type="marcid",
        object_type="rec",
        provider=MarcIdProvider,
        context_cls=Marc21PIDFieldContext,
        # resolver_cls=Resolver,
    )


class Marc21Record(Record):
    """Define API for Marc21 creation and manipulation."""

    model_cls = models.RecordMetadata

    index = IndexField(
        "marc21records-marc21-marc21-v1.0.0", search_alias="marc21records-marc21"
    )

    pid = PIDField(
        key="id",
        pid_type="marcid",
        object_type="rec",
        provider=MarcIdProvider,
        context_cls=Marc21PIDFieldContext,
        # resolver_cls=Resolver,
    )

    conceptpid = PIDField(
        key="conceptid",
        pid_type="marcid",
        object_type="rec",
        provider=MarcIdProvider,
        context_cls=Marc21PIDFieldContext,
        # resolver_cls=Resolver,
    )
