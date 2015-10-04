# -*- coding: utf-8 -*-
"""
    eve-swagger.objects
    ~~~~~~~~~~~~~~~~~~~
    swagger.io extension for Eve-powered REST APIs.

    :copyright: (c) 2015 by Nicola Iarocci.
    :license: BSD, see LICENSE for more details.
"""
from flask import current_app as app

import eve_swagger
from validation import validate_info


def info():
    validate_info()

    cfg = swagger_cfg()['info']

    info = {}
    node(info, 'title', cfg)
    node(info, 'version', cfg)
    node(info, 'description', cfg)
    node(info, 'termsOfService', cfg)

    return info


def host():
    pass


def base_path():
    pass


def schemes():
    pass


def consumes():
    pass


def produces():
    pass


def paths():
    pass


def definitions():
    pass


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


def swagger_cfg():
    return app.config[eve_swagger.SWAGGER]


def node(parent, key, cfg):
    value = cfg.get(key)
    if value:
        parent[key] = cfg[key]
