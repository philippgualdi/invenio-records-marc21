# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2020-2021 CERN.
# Copyright (C) 2020 Northwestern University.
# Copyright (C) 2021 TU Wien.
# Copyright (C) 2021-2023 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Marc21 Record Resource."""


from flask import g
from flask_resources import Resource, resource_requestctx, response_handler, route
from invenio_drafts_resources.resources import RecordResource
from invenio_rdm_records.resources import RDMRecordResource
from invenio_records_resources.resources.errors import ErrorHandlersMixin
from invenio_records_resources.resources.records.resource import (
    request_data,
    request_headers,
    request_view_args,
)

from ..services.record.metadata import Marc21Metadata
from . import config


#
# Records
#
class Marc21RecordResource(RDMRecordResource):
    """Bibliographic record resource."""

    config_name = "MARC21_RECORDS_RECORD_CONFIG"
    default_config = config.Marc21RecordResourceConfig

    def create_url_rules(self):
        """Create the URL rules for the record resource."""
        routes = self.config.routes

        def s(route):
            """Suffix a route with the URL prefix."""
            return f"{route}{self.config.url_prefix}"

        def p(route):
            """Prefix a route with the URL prefix."""
            return f"{self.config.url_prefix}{route}"

        rules = [
            route("GET", p(routes["list"]), self.search),
            route("POST", p(routes["list"]), self.create),
            route("GET", p(routes["item"]), self.read),
            route("PUT", p(routes["item"]), self.update),
            route("DELETE", p(routes["item"]), self.delete),
            route("GET", p(routes["item-versions"]), self.search_versions),
            route("POST", p(routes["item-versions"]), self.new_version),
            route("GET", p(routes["item-latest"]), self.read_latest),
            route("GET", p(routes["item-draft"]), self.read_draft),
            route("POST", p(routes["item-draft"]), self.edit),
            route("PUT", p(routes["item-draft"]), self.update_draft),
            route("DELETE", p(routes["item-draft"]), self.delete_draft),
            route("POST", p(routes["item-publish"]), self.publish),
            # User Dashboard routes
            route("GET", s(routes["user-prefix"]), self.search_user_records),
            # Reviews
            route("GET", p(routes["item-review"]), self.review_read),
            route("PUT", p(routes["item-review"]), self.review_update),
            route("DELETE", p(routes["item-review"]), self.review_delete),
            route("POST", p(routes["item-actions-review"]), self.review_submit),
        ]

        if self.service.draft_files:
            rules.append(
                route(
                    "POST",
                    p(routes["item-files-import"]),
                    self.import_files,
                    apply_decorators=False,
                )
            )

        return rules

    @request_data
    @response_handler()
    def create(self):
        """Create an item."""
        metadata = Marc21Metadata()
        data = resource_requestctx.data
        metadata.xml = data.get("metadata", "")
        data["metadata"] = metadata.json.get("metadata", {})

        item = self.service.create(
            g.identity,
            data=data,
        )
        return item.to_dict(), 201

    @request_headers
    @request_view_args
    @request_data
    @response_handler()
    def update_draft(self):
        """Update a draft.

        PUT /publications/:pid_value/draft
        """
        metadata = Marc21Metadata()
        data = resource_requestctx.data
        metadata.xml = data.get("metadata", "")
        data["metadata"] = metadata.json.get("metadata", {})
        item = self.service.update_draft(
            g.identity,
            resource_requestctx.view_args["pid_value"],
            data,
            revision_id=resource_requestctx.headers.get("if_match"),
        )
        return item.to_dict(), 200

    @request_headers
    @request_view_args
    @request_data  # TODO: probably needs to change
    def review_update(self):
        """Update a review request."""
        type = resource_requestctx.data.pop("type")
        type = f"marc21-{type}"
        resource_requestctx.data["type"] = type

        item = self.service.review.update(
            g.identity,
            resource_requestctx.view_args["pid_value"],
            resource_requestctx.data,
            revision_id=resource_requestctx.headers.get("if_match"),
        )

        return item.to_dict(), 200

    @request_headers
    @request_view_args
    @request_data
    def review_submit(self):
        """Submit a draft for review or directly publish it."""
        require_review = False
        if resource_requestctx.data:
            require_review = resource_requestctx.data.pop("require_review", False)

        item = self.service.review.submit(
            g.identity,
            resource_requestctx.view_args["pid_value"],
            resource_requestctx.data,
            require_review=require_review,
        )
        return item.to_dict(), 202



class Marc21ParentRecordLinksResource(RecordResource):
    """Marc21 parent publication resource."""

    def create_url_rules(self):
        """Create the URL rules for the record resource."""

        def p(route):
            """Prefix a route with the URL prefix."""
            return f"{self.config.url_prefix}{route}"

        routes = self.config.routes
        return [
            route("GET", p(routes["list"]), self.search),
            route("POST", p(routes["list"]), self.create),
            route("GET", p(routes["item"]), self.read),
            route("PUT", p(routes["item"]), self.update),
            route("DELETE", p(routes["item"]), self.delete),
        ]


class Marc21RecordCommunitiesResource(ErrorHandlersMixin, Resource):
    """Marc21 communities publication resource."""

    def __init__(self, config, service):
        """Constructor."""
        super().__init__(config)
        self.service = service

    def create_url_rules(self):
        """Create the URL rules for the record resource."""
        routes = self.config.routes
        url_rules = [
            route("GET", routes["list"], self.search),
            route("GET", routes["suggestions"], self.get_suggestions),
        ]
        return url_rules
