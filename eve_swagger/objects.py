# -*- coding: utf-8 -*-
"""
    eve-swagger.objects
    ~~~~~~~~~~~~~~~~~~~
    swagger.io extension for Eve-powered REST APIs.

    :copyright: (c) 2015 by Nicola Iarocci.
    :license: BSD, see LICENSE for more details.
"""
from collections import OrderedDict
from eve.utils import api_prefix
from flask import request, current_app as app

import eve_swagger
from .validation import validate_info


def info():
    validate_info()

    cfg = app.config[eve_swagger.INFO]

    def node(parent, cfg, key):
        value = cfg.get(key)
        if value:
            parent[key] = cfg[key]

    info = OrderedDict()
    node(info, cfg, 'title')
    node(info, cfg, 'description')
    node(info, cfg, 'termsOfService')
    node(info, cfg, 'contact')
    node(info, cfg, 'license')
    node(info, cfg, 'version')

    return info


def host():
    # TODO should probably return None if 'host' has not been set as the host
    # is optional in swagger.
    return app.config.get(eve_swagger.HOST) or request.host


def base_path():
    return api_prefix()


def schemes():
    scheme = request.url.split(':')[0]
    return [scheme] if scheme in ['http', 'https', 'ws', 'wss'] else None


def consumes():
    return ['application/json']


def produces():
    produces = []
    if app.config.get('XML', True):
        produces.append('application/xml')
    if app.config.get('JSON', True):
        produces.append('application/json')
    return produces if produces else None


def parameters():
    pass


def responses():
    pass


def security_definitions():
    pass


def security():
    pass


def tags():
    pass


def external_docs():
    pass
