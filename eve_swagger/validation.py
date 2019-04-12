# -*- coding: utf-8 -*-
"""
    eve-swagger.validation
    ~~~~~~~~~~~~~~~~~~~~~~
    swagger.io extension for Eve-powered REST APIs.

    :copyright: (c) 2015 by Nicola Iarocci.
    :license: BSD, see LICENSE for more details.
"""
from eve.exceptions import ConfigException
from flask import current_app as app
from cerberus import Validator

import eve_swagger

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse


def validate_info():
    v = Validator()
    schema = {
        'title': {'required': True, 'type': 'string'},
        'version': {'required': True, 'type': 'string'},
        'description': {'type': 'string'},
        'termsOfService': {'type': 'string'},
        'contact': {
            'type': 'dict',
            'schema': {
                'name': {'type': 'string'},
                'url': {'type': 'string', 'validator': _validate_url},
                'email': {
                    'type': 'string',
                    'regex':
                    r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
                }
            }
        },
        'license': {
            'type': 'dict',
            'schema': {
                'name': {'type': 'string', 'required': True},
                'url': {'type': 'string', 'validator': _validate_url}
            }
        },
        'schemes': {
            'type': 'list',
            'schema': {
                'type': 'string'
            }
        }
    }
    if eve_swagger.INFO not in app.config:
        raise ConfigException('%s setting is required in Eve configuration.' %
                              eve_swagger.INFO)

    if not v.validate(app.config[eve_swagger.INFO], schema):
        raise ConfigException('%s is misconfigured: %s' % (
            eve_swagger.INFO, v.errors))


def _validate_url(field, value, error):
    # TODO probably too weak
    o = urlparse(value)
    if not bool(o.scheme):
        error(field, 'Invalid URL')
