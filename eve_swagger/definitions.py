# -*- coding: utf-8 -*-
"""
    eve-swagger.definitions
    ~~~~~~~~~~~~~~~~~~~~~~~
    swagger.io extension for Eve-powered REST APIs.

    :copyright: (c) 2016 by Nicola Iarocci.
    :license: BSD, see LICENSE for more details.
"""
from collections import OrderedDict
from flask import current_app as app


def definitions():
    definitions = OrderedDict()
    for rd in app.config['DOMAIN'].values():
        title = rd['item_title']
        definitions[title] = _object(rd['schema'])

    return definitions


def _object(schema):
    props = {}
    required = []
    for field, rules in schema.items():
        if rules.get('required') is True:
            required.append(field)

        props[field] = _type_and_format(rules)

    field_def = {}
    field_def['type'] = 'object'
    field_def['properties'] = props
    if len(required):
        field_def['required'] = required
    return field_def


def _type_and_format(rules):
    resp = {}
    map = {
        'dict': ('object',),
        'list': ('array',),
        'objectid': ('string', 'objectid'),
        'datetime': ('string', 'date-time'),
    }

    eve_type = rules['type']
    type = map.get(eve_type, (eve_type,))

    resp['type'] = type[0]
    if type[0] == 'object':
        # we don't support 'valueschema' rule
        if 'schema' in rules:
            resp.update(_object(rules['schema']))
    elif type[0] == 'array':
        type = 'array'
        if 'schema' in rules:
            resp['items'] = _object(rules['schema'])
        else:
            # 'items' is mandatory for swagger, we assume it's a list of
            # strings
            resp['items'] = {'type': 'string'}
    else:
        try:
            resp['format'] = type[1]
        except IndexError:
            pass

    return resp
