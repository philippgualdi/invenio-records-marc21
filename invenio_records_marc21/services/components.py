# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


"""Marc21 service components."""

from invenio_drafts_resources.services.records.components import (
    PIDComponent as BasePIDComponent,
)
from invenio_records_resources.services.records.components import ServiceComponent


class AccessComponent(ServiceComponent):
    """Service component for access integration."""

    def create(self, identity, data=None, record=None, **kwargs):
        """Add basic ownership fields to the record."""
        validated_data = data.get("access", {})
        # TODO (Alex): replace with `record.access = ...`
        if identity.id:
            validated_data.setdefault("owned_by", [{"user": identity.id}])
        record.update({"access": validated_data})

    def update(self, identity, data=None, record=None, **kwargs):
        """Update handler."""
        validated_data = data.get("access", {})
        # TODO (Alex): replace with `record.access = ...`
        if identity.id:
            validated_data.setdefault("owned_by", [{"user": identity.id}])
        record.update({"access": validated_data})


class PIDComponent(BasePIDComponent):
    """Service component for pids integration."""

    def create(self, identity, data=None, record=None, **kwargs):
        """Create PID when record is created.."""
        # We create the PID after all the data has been initialized. so that
        # we can rely on having the 'id' and type set.
        self.service.record_cls.pid.create(record)
