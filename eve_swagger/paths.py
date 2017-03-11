# -*- coding: utf-8 -*-
"""
    eve-swagger.paths
    ~~~~~~~~~~~~~~~~~
    swagger.io extension for Eve-powered REST APIs.

    :copyright: (c) 2015 by Nicola Iarocci.
    :license: BSD, see LICENSE for more details.
"""
from textwrap import dedent

from flask import current_app as app

from eve_swagger import OrderedDict


# TODO consider adding at least a 'schema' property to response objects
# TODO take auth into consideration


def paths():
    paths = OrderedDict()
    for resource, rd in app.config['DOMAIN'].items():
        if (rd.get('disable_documentation')
                or resource.endswith('_versions')):
            continue

        methods = rd['resource_methods']
        if methods:
            url = '/%s' % rd['url']
            paths[url] = _resource(resource, rd, methods)

        methods = rd['item_methods']
        if methods:
            item_id = '%sId' % rd['item_title'].lower()
            url = '/%s/{%s}' % (rd['url'], item_id)
            paths[url] = _item(resource, rd, methods)

    return paths


def _resource(resource, rd, methods):
    item = OrderedDict()
    describe_hooks = app.config.get('ENABLE_HOOK_DESCRIPTION', False)
    if 'GET' in methods:
        item['get'] = get_response(rd)
    if 'POST' in methods:
        item['post'] = post_response(rd)
    if 'DELETE' in methods:
        item['delete'] = delete_response(rd)

    if describe_hooks:
        for m in methods:
            hook_desc = _hook_descriptions(resource, m)
            if hook_desc != '':
                item[m.lower()]['description'] = '**Hooks**:' + hook_desc

    return item


def _item(resource, rd, methods):
    item = OrderedDict()
    describe_hooks = app.config.get('ENABLE_HOOK_DESCRIPTION', False)
    if 'GET' in methods:
        item['get'] = getitem_response(rd)
    if 'PUT' in methods:
        item['put'] = put_response(rd)
    if 'PATCH' in methods:
        item['patch'] = patch_response(rd)
    if 'DELETE' in methods:
        item['delete'] = deleteitem_response(rd)

    if describe_hooks:
        for m in methods:
            hook_desc = _hook_descriptions(resource, m, item=True)
            if hook_desc != '':
                item[m.lower()]['description'] = '**Hooks**:' + hook_desc

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
                'items': get_ref_schema(rd)}}}),
        ('tags', [rd['item_title']])
    ])


def post_response(rd):
    return OrderedDict([
        ('summary', 'Stores one or more %s' % rd['resource_title']),
        ('parameters', [get_parameters(rd)]),
        ('responses', {'201':
                       {'description': 'operation has been successful'}}),
        ('tags', [rd['item_title']])
    ])


def delete_response(rd):
    return OrderedDict([
        ('summary', 'Deletes all %s' % rd['resource_title']),
        ('responses', {'204':
                       {'description': 'operation has been successful'}}),
        ('tags', [rd['item_title']])
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
        ('parameters', [id_parameter(rd)]),
        ('tags', [rd['item_title']])
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
        ('parameters', [id_parameter(rd),
                        get_parameters(rd),
                        header_parameters()]),
        ('tags', [rd['item_title']])
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
        ('parameters', [id_parameter(rd),
                        get_parameters(rd),
                        header_parameters()]),
        ('tags', [rd['item_title']])
    ])


def deleteitem_response(rd):
    title = rd['item_title']
    return OrderedDict([
        ('summary', 'Deletes a %s document' % title),
        ('responses', {
            '204': {
                'description': '%s document deleted successfully' % title
            }
        }),
        ('parameters', [id_parameter(rd), header_parameters()]),
        ('tags', [rd['item_title']])
    ])


def id_parameter(rd):
    return {'$ref': '#/parameters/{0}_{1}'.format(rd['item_title'],
                                                  rd['item_lookup_field'])}


def header_parameters():
    r = OrderedDict()
    r['in'] = 'header'
    r['name'] = 'If-Match'
    r['description'] = 'Current value of the _etag field'
    r['required'] = True
    r['type'] = 'string'
    return r


def _hook_descriptions(resource, method, item=False):
    if method == 'GET':
        if item is True:
            events = ['on_pre_GET',
                      'on_pre_GET_' + resource,
                      'on_fetched_item',
                      'on_fetched_item_' + resource,
                      'on_post_GET',
                      'on_post_GET_' + resource]
        else:
            events = ['on_pre_GET',
                      'on_pre_GET_' + resource,
                      'on_fetched_resource',
                      'on_fetched_resource_' + resource,
                      'on_post_GET',
                      'on_post_GET_' + resource]

    if method == 'POST':
        events = ['on_pre_POST',
                  'on_pre_POST_' + resource,
                  'on_insert',
                  'on_insert_' + resource,
                  'on_inserted',
                  'on_inserted_' + resource,
                  'on_post_POST',
                  'on_post_POST_' + resource]
    if method == 'PUT':
        events = ['on_pre_PUT',
                  'on_pre_PUT_' + resource,
                  'on_replace',
                  'on_replace_' + resource,
                  'on_replaced',
                  'on_replaced_' + resource,
                  'on_post_PUT',
                  'on_post_PUT_' + resource]
    if method == 'PATCH':
        events = ['on_pre_PATCH',
                  'on_pre_PATCH_' + resource,
                  'on_update',
                  'on_update_' + resource,
                  'on_updated',
                  'on_updated_' + resource,
                  'on_post_PATCH',
                  'on_post_PATCH_' + resource]
    if method == 'DELETE':
        if item is True:
            events = ['on_pre_DELETE',
                      'on_pre_DELETE_' + resource,
                      'on_delete_item',
                      'on_delete_item_' + resource,
                      'on_deleted_item',
                      'on_deleted_item_' + resource,
                      'on_post_DELETE',
                      'on_post_DELETE_' + resource]
        else:
            events = ['on_pre_DELETE',
                      'on_pre_DELETE_' + resource,
                      'on_delete_resource',
                      'on_delete_resource_' + resource,
                      'on_deleted_resource',
                      'on_deleted_resource_' + resource,
                      'on_post_DELETE',
                      'on_post_DELETE_' + resource]

    res = ''
    for e in events:
        callbacks = getattr(app, e)
        if len(callbacks) > 0:
            res += '\n* `' + e + '`:\n\n'
        for cb in callbacks:
            if cb.__doc__:
                s = '\n    '
                s += '\n    '.join(dedent(cb.__doc__).strip().split('\n'))
                res += '  * `' + cb.__name__ + '`:\n' + s + '\n\n'
            else:
                # there is no docstring provided, still add the hook name for
                # information
                res += '  * `' + cb.__name__ + '`:\nno documentation\n\n'
    return res
