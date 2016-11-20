# -*- coding: utf-8 -*-
"""
    eve-swagger.swagger
    ~~~~~~~~~~~~~~~~~~~
    swagger.io extension for Eve-powered REST APIs.

    :copyright: (c) 2015 by Nicola Iarocci.
    :license: BSD, see LICENSE for more details.
"""
import re
from collections import Mapping
from flask import Blueprint, jsonify, make_response, request, \
    current_app as app
from functools import wraps

from eve_swagger import OrderedDict
from .definitions import definitions
from .objects import info, host, base_path, schemes, consumes, produces, \
    parameters, responses, security_definitions, security, tags, \
    external_docs
from .paths import paths


swagger = Blueprint('eve_swagger', __name__)
swagger.additional_documentation = OrderedDict()


def add_documentation(doc):
    _nested_update(swagger.additional_documentation, doc)


def _modify_response(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if request.method == 'OPTIONS':
            resp = app.make_default_options_response()
        else:
            resp = make_response(f(*args, **kwargs))

        # CORS
        domains = app.config.get('X_DOMAINS')
        headers = app.config.get('X_HEADERS')
        max_age = app.config.get('X_MAX_AGE')
        allow_credentials = app.config.get('X_ALLOW_CREDENTIALS')
        expose_headers = app.config.get('X_EXPOSE_HEADERS')
        origin = request.headers.get('Origin')
        if origin and domains:
            if isinstance(domains, str):
                domains = [domains]

            if headers is None:
                headers = []
            elif isinstance(headers, str):
                headers = [headers]

            if expose_headers is None:
                expose_headers = []
            elif isinstance(expose_headers, str):
                expose_headers = [expose_headers]

            allow_credentials = allow_credentials is True
            methods = app.make_default_options_response().headers.get(
                'allow', '')

            h = resp.headers
            if '*' in domains:
                h['Access-Control-Allow-Origin'] = origin
                h['Vary'] = 'Origin'
            elif any(re.match(re.escape(domain), origin)
                     for domain in domains):
                h['Access-Control-Allow-Origin'] = origin
            else:
                h['Access-Control-Allow-Origin'] = ''

            h['Access-Control-Allow-Headers'] = ', '.join(headers)
            h['Access-Control-Expose-Headers'] = ', '.join(expose_headers)
            h['Access-Control-Allow-Methods'] = methods
            h['Access-Control-Max-Age'] = str(max_age)

        return resp
    return decorated


@swagger.route('/api-docs')
@_modify_response
def index():
    def node(parent, key, value):
        if value:
            parent[key] = value

    root = OrderedDict()
    root['swagger'] = '2.0'
    node(root, 'info', info())
    node(root, 'host', host())
    node(root, 'basePath', base_path())
    node(root, 'schemes', schemes())
    node(root, 'consumes', consumes())
    node(root, 'produces', produces())
    node(root, 'paths', paths())
    node(root, 'definitions', definitions())
    node(root, 'parameters', parameters())
    node(root, 'responses', responses())
    node(root, 'securityDefinitions', security_definitions())
    node(root, 'security', security())
    node(root, 'tags', tags())
    node(root, 'externalDocs', external_docs())

    _nested_update(root, swagger.additional_documentation)

    return jsonify(root)


def _nested_update(orig_dict, new_dict):
    for key, val in new_dict.items():
        if isinstance(val, Mapping):
            tmp = _nested_update(orig_dict.get(key, {}), val)
            orig_dict[key] = tmp
        elif isinstance(val, list):
            orig_dict[key] = (orig_dict.get(key, []) + val)
        else:
            orig_dict[key] = new_dict[key]
    return orig_dict
