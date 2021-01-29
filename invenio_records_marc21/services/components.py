# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


"""Marc21 service components."""

from datetime import date

from invenio_records_resources.services.records.components import ServiceComponent


class AccessComponent(ServiceComponent):
    """Service component for access integration."""

    def set_default(self, identity, data=None, record=None):
        validated_data = data.get("access", {})
        validated_data.setdefault("access_right", False)
        validated_data.setdefault("owned_by", [identity.id])
        validated_data.setdefault("access_right", "open")
        validated_data.setdefault("embargo_date", date.today().strftime("%Y-%m-%d"))
        record.update({"access": validated_data})

    def create(self, identity, data=None, record=None, **kwargs):
        """Add basic ownership fields to the record."""
        self.set_default(identity, data, record)

    def update(self, identity, data=None, record=None, **kwargs):
        """Update handler."""
        self.set_default(identity, data, record)
