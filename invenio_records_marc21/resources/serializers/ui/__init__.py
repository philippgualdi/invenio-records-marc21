# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


"""Record response serializers."""

from flask_resources.serializers import JSONSerializer

from .schema import UIListSchema, UIObjectSchema


class UIJSONSerializer(JSONSerializer):
    """UI JSON serializer implementation."""

    object_key = "ui"
    object_schema_cls = UIObjectSchema
    list_schema_cls = UIListSchema

    #
    # Dump Python dictionary (obj and list)
    #
    def dump_obj(self, obj):
        """Dump the object with extra information."""
        obj[self.object_key] = self.object_schema_cls().dump(obj)
        return obj

    def dump_list(self, obj_list):
        """Dump the list of objects with extra information."""
        ctx = {
            "object_key": self.object_key,
            "object_schema_cls": self.object_schema_cls,
        }
        return self.list_schema_cls(context=ctx).dump(obj_list)

    #
    # Serialize to  JSON (obj and list)
    #
    def serialize_object(self, obj):
        """Dump the object into a JSON string."""
        return super().serialize_object(self.dump_obj(obj))

    def serialize_object_list(self, obj_list):
        """Dump the object list into a JSON string."""
        return super().serialize_object_list(self.dump_list(obj_list))

    def serialize_object_to_dict(self, obj):
        """Dump the object into a JSON string."""
        return self.dump_obj(obj)

    def serialize_object_list_to_dict(self, obj_list):
        """Dump the object list into a JSON string."""
        return self.dump_list(obj_list)
