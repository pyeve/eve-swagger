# -*- coding: utf-8 -*-
"""
    eve-swagger.objects
    ~~~~~~~~~~~~~~~~~~~
    swagger.io extension for Eve-powered REST APIs.

    :copyright: (c) 2015 by Nicola Iarocci.
    :license: BSD, see LICENSE for more details.
"""
from eve.utils import api_prefix
from flask import request, current_app as app

import eve_swagger
from eve_swagger import OrderedDict
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
    cfg = app.config[eve_swagger.INFO]
    if hasattr(cfg, 'schemes'):
        return cfg['schemes']

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
    parameters = OrderedDict()
    for (resource_name, rd) in app.config['DOMAIN'].items():
        if (resource_name.endswith('_versions')
                or rd.get('disable_documentation')):
            continue

        title = rd['item_title']
        lookup_field = rd['item_lookup_field']
        if lookup_field not in rd['schema']:
            rd['schema'][lookup_field] = {'type': 'objectid'}
        eve_type = rd['schema'][lookup_field]['type']
        descr = rd['schema'][lookup_field].get('description') or ''
        if 'data_relation' in rd['schema'][lookup_field]:
            # the lookup field is a copy of another field
            dr = rd['schema'][lookup_field]['data_relation']

            # resource definition of the data relation source
            source_rd = app.config['DOMAIN'][dr['resource']]

            # schema of the data relation source field
            source_def = source_rd['schema'][dr['field']]

            # key in #/definitions/...
            source_def_name = source_rd['item_title']+'_'+dr['field']

            # copy description if necessary
            descr = descr or source_def.get('description')
            descr = descr + ' (links to {0})'.format(source_def_name)

        p = OrderedDict()
        p['in'] = 'path'
        p['name'] = title.lower() + 'Id'
        p['required'] = True
        p['description'] = descr
        p['type'] = eve_type
        if eve_type == 'objectid':
            p['type'] = 'string'
            p['format'] = 'objectid'
        elif eve_type == 'datetime':
            p['type'] = 'string'
            p['format'] = 'date-time'
        elif eve_type == 'float':
            p['type'] = 'number'
            p['format'] = 'float'

        parameters[title+'_'+lookup_field] = p

    return parameters


def responses():
    pass


def security_definitions():
    pass


def security():
    pass


def tags():
    tags = []
    for (resource_name, rd) in app.config['DOMAIN'].items():
        if (resource_name.endswith('_versions')
                or rd.get('disable_documentation')):
            continue

        tagInfo = {"name": rd['item_title']}

        if 'description' in rd:
            tagInfo['description'] = rd['description']

        tags.append(tagInfo)
    return tags


def external_docs():
    pass
