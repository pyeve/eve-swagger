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
    dr_sources = {}
    for rd in app.config['DOMAIN'].values():
        dr_sources.update(_get_dr_sources(rd['schema']))

    for rd in app.config['DOMAIN'].values():
        if rd.get('disable_documentation'):
            continue
        title = rd['item_title']
        definitions[title] = _object(rd, dr_sources)
        if 'description' in rd:
            definitions[title]['description'] = rd['description']

    # add data_relation source fields to #/definitions/
    definitions.update(dr_sources)
    return definitions


def _object(rd, dr_sources):
    props = {}
    required = []
    for field, rules in rd['schema'].items():
        if rules.get('required') is True:
            required.append(field)

        def_name = rd['item_title']+'_'+field
        props[field] = _field_props(rules, dr_sources, def_name)

        if def_name in dr_sources:
            # the current field is a source of a data_relation

            # replace None in dr_sources with the field properties
            dr_sources[def_name] = OrderedDict(props[field])

            props[field] = {'$ref': '#/definitions/{}'.format(def_name)}

        if 'data_relation' in rules:
            # the current field is a copy of another field
            dr = rules['data_relation']
            if dr['resource'] not in app.config['DOMAIN']:
                # source of data_relation does not exist
                continue
            title = app.config['DOMAIN'][dr['resource']]['item_title']
            source_def_name = title+'_'+dr['field']
            props[field] = {'$ref': '#/definitions/{}'.format(source_def_name)}

    field_def = {}
    field_def['type'] = 'object'
    field_def['properties'] = props
    if len(required):
        field_def['required'] = required
    return field_def


def _field_props(rules, dr_sources, prefix):
    resp = {}
    map = {
        'dict': ('object',),
        'list': ('array',),
        'objectid': ('string', 'objectid'),
        'datetime': ('string', 'date-time'),
        'float': ('number', 'float'),
    }

    eve_type = rules.get('type')
    if eve_type is None:
        return resp

    if 'description' in rules:
        resp['description'] = rules['description']

    if 'allowed' in rules:
        resp['enum'] = rules['allowed']

    if 'default' in rules:
        resp['default'] = rules['default']

    if 'minlength' in rules:
        if eve_type == 'string':
            resp['minLength'] = rules['minlength']
        elif eve_type == 'list':
            resp['minItems'] = rules['minlength']

    if 'maxlength' in rules:
        if eve_type == 'string':
            resp['maxLength'] = rules['maxlength']
        elif eve_type == 'list':
            resp['maxItems'] = rules['maxlength']

    if 'min' in rules:
        if eve_type in ['number', 'integer', 'float']:
            resp['minimum'] = rules['min']

    if 'max' in rules:
        if eve_type in ['number', 'integer', 'float']:
            resp['maximum'] = rules['max']

    type = map.get(eve_type, (eve_type,))

    resp['type'] = type[0]
    if type[0] == 'object':
        # we don't support 'valueschema' rule
        if 'schema' in rules:
            # set prefix as item_title to avoid name collisions of nested
            # fields with higher up fields
            pseudo_rd = {'item_title': prefix, 'schema': rules['schema']}
            resp.update(_object(pseudo_rd, dr_sources))
    elif type[0] == 'array':
        type = 'array'
        if 'schema' in rules:
            resp['items'] = _field_props(rules['schema'], dr_sources, prefix)
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


def _get_dr_sources(schema):
    '''
    Returns a dict of names for sources of data_relations:

    e.g. the name field in the user resource relates to (is a copy of) the
    name field of the person resource
    => return {'person_name': None}
    '''
    dr_sources = {}
    for rules in schema.values():
        if 'data_relation' in rules:
            dr = rules['data_relation']
            if dr['resource'] not in app.config['DOMAIN']:
                # source of data_relation does not exist
                continue
            title = app.config['DOMAIN'][dr['resource']]['item_title']
            def_name = title+'_'+dr['field']
            dr_sources[def_name] = None
        elif 'schema' in rules and rules.get('type') == 'dict':
            # recursively handle data_relations in subdicts
            dr_sources.update(_get_dr_sources(rules['schema']))
    return dr_sources
