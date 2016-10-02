# -*- coding: utf-8 -*-
"""
    eve-swagger.paths
    ~~~~~~~~~~~~~~~~~
    swagger.io extension for Eve-powered REST APIs.

    :copyright: (c) 2015 by Nicola Iarocci.
    :license: BSD, see LICENSE for more details.
"""
from eve_swagger import OrderedDict
from flask import current_app as app

# TODO consider adding at least a 'schema' property to response objects
# TODO take auth into consideration


def paths():
    paths = OrderedDict()
    for rd in app.config['DOMAIN'].values():
        if rd.get('disable_documentation'):
            continue
        methods = rd['resource_methods']
        if methods:
            url = '/%s' % rd['url']
            paths[url] = _resource(rd, methods)

        methods = rd['item_methods']
        if methods:
            item_id = '%sId' % rd['item_title'].lower()
            url = '/%s/{%s}' % (rd['url'], item_id)
            paths[url] = _item(rd, methods)
    return paths


def _resource(rd, methods):
    item = OrderedDict()
    if 'GET' in methods:
        item['get'] = get_response(rd)
    if 'POST' in methods:
        item['post'] = post_response(rd)
    if 'DELETE' in methods:
        item['delete'] = delete_response(rd)
    return item


def _item(rd, methods):
    item = OrderedDict()
    if 'GET' in methods:
        item['get'] = getitem_response(rd)
    if 'PUT' in methods:
        item['put'] = put_response(rd)
    if 'PATCH' in methods:
        item['patch'] = patch_response(rd)
    if 'DELETE' in methods:
        item['delete'] = deleteitem_response(rd)
    return item


def get_ref_schema(rd):
    return {'$ref': '#/definitions/%s' % rd['item_title']}


def get_parameters(rd):
    return OrderedDict([
        ('in', 'body'),
        ('name', rd['item_title']),
        ('required', True),
        ('schema', get_ref_schema(rd)),
    ])


def get_response(rd):
    title = rd['resource_title']
    return OrderedDict([
        ('summary', 'Retrieves one or more %s' % title),
        ('responses', {'200': {
            'description': 'An array of %s' % title,
            'schema': {
                'type': 'array',
                'items': get_ref_schema(rd)}}})
    ])


def post_response(rd):
    return OrderedDict([
        ('summary', 'Stores one or more %s' % rd['resource_title']),
        ('parameters', [get_parameters(rd)]),
        ('responses', {'200':
                       {'description': 'operation has been successful'}})
    ])


def delete_response(rd):
    return OrderedDict([
        ('summary', 'Deletes all %s' % rd['resource_title']),
        ('responses', {'200':
                       {'description': 'operation has been successful'}}),
    ])


def getitem_response(rd):
    title = rd['item_title']
    return OrderedDict([
        ('summary', 'Retrieves a %s document' % title),
        ('responses', {
            '200': {
                'description': '%s document fetched successfully' % title,
                'schema': get_ref_schema(rd)
            },

        }),
        ('parameters', [id_parameter(rd)])
    ])


def put_response(rd):
    title = rd['item_title']
    return OrderedDict([
        ('summary', 'Replaces a %s document' % title),
        ('responses', {
            '200': {
                'description': '%s document replaced successfully' % title
            }
        }),
        ('parameters', [id_parameter(rd), get_parameters(rd)])
    ])


def patch_response(rd):
    title = rd['item_title']
    return OrderedDict([
        ('summary', 'Updates a %s document' % title),
        ('responses', {
            '200': {
                'description': '%s document updated successfully' % title
            }
        }),
        ('parameters', [id_parameter(rd), get_parameters(rd)])
    ])


def deleteitem_response(rd):
    title = rd['item_title']
    return OrderedDict([
        ('summary', 'Deletes a %s document' % title),
        ('responses', {
            '200': {
                'description': '%s document deleted successfully' % title
            }
        }),
        ('parameters', [id_parameter(rd)])
    ])


def id_parameter(rd):
    return {'$ref': '#/parameters/{}_{}'.format(rd['item_title'],
                                                rd['item_lookup_field'])}
