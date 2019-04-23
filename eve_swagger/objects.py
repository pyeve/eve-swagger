# -*- coding: utf-8 -*-
"""
    eve-swagger.objects
    ~~~~~~~~~~~~~~~~~~~
    swagger.io extension for Eve-powered REST APIs.

    :copyright: (c) 2015 by Nicola Iarocci.
    :license: BSD, see LICENSE for more details.
"""
from collections import OrderedDict
from flask import request, current_app as app

import eve_swagger
from .validation import validate_info
from .paths import get_ref_schema


def _get_scheme():
    return "http" if app.auth is None else "https"


def info():
    validate_info()

    cfg = app.config[eve_swagger.INFO]

    def node(parent, cfg, key):
        value = cfg.get(key)
        if value:
            parent[key] = cfg[key]

    info = OrderedDict()
    node(info, cfg, "title")
    node(info, cfg, "description")
    node(info, cfg, "termsOfService")
    node(info, cfg, "contact")
    node(info, cfg, "license")
    node(info, cfg, "version")

    return info


def servers():
    return [
        {
            "url": "%s://" % _get_scheme()
            + (app.config.get(eve_swagger.HOST) or request.host)
        }
    ]


def responses():
    return {
        "error": {
            "description": "An error message",
            "content": {
                "application/json": {"schema": {"$ref": "#/components/schemas/Error"}}
            },
        }
    }


def parameters():
    parameters = OrderedDict()
    # resource parameters
    for (resource_name, rd) in app.config["DOMAIN"].items():
        if resource_name.endswith("_versions") or rd.get("disable_documentation"):
            continue

        title = rd["item_title"]
        lookup_field = rd["item_lookup_field"]
        if lookup_field not in rd["schema"]:
            rd["schema"][lookup_field] = {"type": "objectid"}
        eve_type = rd["schema"][lookup_field]["type"]
        descr = rd["schema"][lookup_field].get("description") or ""
        example = rd["schema"][lookup_field].get("example") or ""
        if "data_relation" in rd["schema"][lookup_field]:
            # the lookup field is a copy of another field
            dr = rd["schema"][lookup_field]["data_relation"]

            # resource definition of the data relation source
            source_rd = app.config["DOMAIN"][dr["resource"]]

            # schema of the data relation source field
            source_def = source_rd["schema"][dr["field"]]

            # key in #/definitions/...
            source_def_name = source_rd["item_title"] + "_" + dr["field"]

            # copy description if necessary
            descr = descr or source_def.get("description")
            descr = descr + " (links to {})".format(source_def_name)

        p = OrderedDict()
        p["in"] = "path"
        p["name"] = title.lower() + "Id"
        p["required"] = True
        p["description"] = descr
        p["example"] = example

        ptype = ""
        if eve_type == "objectid" or eve_type == "datetime":
            ptype = "string"
        elif eve_type == "float":
            ptype = "number"
        else:
            # TODO define default
            pass

        p["schema"] = {"type": ptype}
        parameters[title + "_" + lookup_field] = p

    # add header parameters
    parameters.update(_header_parameters())

    return parameters


def _header_parameters():
    r = OrderedDict()
    r["in"] = "header"
    r["name"] = "If-Match"
    r["description"] = "Current value of the _etag field"
    r["required"] = app.config["IF_MATCH"] and app.config["ENFORCE_IF_MATCH"]
    r["schema"] = {"type": "string"}
    return {"If-Match": r}


def examples():
    examples = OrderedDict()

    for (resource_name, rd) in app.config["DOMAIN"].items():
        if resource_name.endswith("_versions") or rd.get("disable_documentation"):
            continue

        title = rd["item_title"]
        ex = OrderedDict()
        ex["summary"] = "An example {0} document."
        ex["description"] = (
            "An example for {0} documents request bodies."
            " Used in POST, PUT, PATCH methods."
        ).format(title)
        if "example" in rd:
            ex["value"] = rd["example"]

        examples[title] = ex

    return examples


def request_bodies():
    def _get_ref_examples(rd):
        return {"$ref": "#/components/examples/%s" % rd["item_title"]}

    rbodies = OrderedDict()

    for (resource_name, rd) in app.config["DOMAIN"].items():
        if resource_name.endswith("_versions") or rd.get("disable_documentation"):
            continue

        title = rd["item_title"]
        rb = OrderedDict()
        description = "A {} document.".format(title)
        if rd["bulk_enabled"]:
            description = "A {0} or list of {0} documents".format(title)

        rb["description"] = description
        rb["required"] = True
        rb["content"] = {
            # TODO what about other methods
            "application/json": {
                "schema": get_ref_schema(rd),
                "examples": {title: _get_ref_examples(rd)}
                # {
                #    title: ,
                # }
            }
        }
        rbodies[title] = rb

    return rbodies


def headers():
    pass


def security_schemes():
    if app.auth is not None:
        # TODO use app.auth to build the security scheme
        return {
            "oAuth2": {
                "type": "oauth2",
                "description": "oAuth2 password credentials.",
                "flows": {
                    "password": {
                        # TODO why does this not work with a relative path?
                        "tokenUrl": "%s://" % _get_scheme()
                        + app.config["SERVER_NAME"]
                        + app.config["SENTINEL_ROUTE_PREFIX"]
                        + app.config["SENTINEL_TOKEN_URL"],
                        "scopes": {},
                    }
                },
            }
        }


def links():
    pass


def callbacks():
    pass


def security():
    return [{"oAuth2": []}]


def tags():
    tags = []
    for (resource_name, rd) in app.config["DOMAIN"].items():
        if resource_name.endswith("_versions") or rd.get("disable_documentation"):
            continue

        tagInfo = {"name": rd["item_title"]}

        if "description" in rd:
            tagInfo["description"] = rd["description"]

        tags.append(tagInfo)
    return tags


def external_docs():
    pass
