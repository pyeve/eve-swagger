# -*- coding: utf-8 -*-
"""
    eve-swagger.swagger
    ~~~~~~~~~~~~~~~~~~~
    swagger.io extension for Eve-powered REST APIs.

    :copyright: (c) 2015 by Nicola Iarocci.
    :license: BSD, see LICENSE for more details.
"""
from collections import OrderedDict
from flask import Blueprint, jsonify

from .objects import info, host, base_path, schemes, consumes, produces, \
    definitions, parameters, responses, security_definitions, security, \
    tags, external_docs
from .paths import paths


swagger = Blueprint('eve_swagger', __name__)


@swagger.route('/api-docs')
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

    return jsonify(root)
