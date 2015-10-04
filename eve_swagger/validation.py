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

import eve_swagger


def validate_info():
    _validate_required('info')
    _validate_required('info.title')
    _validate_required('info.version')


def _validate_required(key):
    key = '%s.%s' % (eve_swagger.SWAGGER, key)
    node = app.config

    parts = key.split('.')
    for part in parts:
        if part not in node:
            raise ConfigException('%s is required' % key)
        node = node[part]
