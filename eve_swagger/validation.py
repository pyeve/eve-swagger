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
import urllib

import eve_swagger


def validate_info():
    _validate_required('info')
    info = app.config[eve_swagger.SWAGGER].get('info')

    allowed = [
        'title',
        'description',
        'termsOfService',
        'contact',
        'license',
        'version'
    ]
    _validate_document(info, 'info', allowed)

    _validate_required('info.title')
    _validate_required('info.version')

    def validate_contact():
        contact = info.get('contact')
        if contact is None:
            return

        allowed = [
            'name',
            'url',
            'email'
        ]
        _validate_document(contact, 'info.contact', allowed)
        _validate_url(contact.get('url'), 'info.contact.url')
        _validate_email(contact.get('email'), 'info.contact.email')

    def validate_license():
        license = info.get('license')
        if license is None:
            return

        allowed = [
            'name',
            'url'
        ]
        _validate_document(license, 'info.license', allowed)
        _validate_required('info.license.name')
        _validate_url(license.get('url'), 'info.license.url')

    validate_contact()
    validate_license()


def _validate_required(key):
    key = '%s.%s' % (eve_swagger.SWAGGER, key)
    node = app.config

    parts = key.split('.')
    for part in parts:
        if part not in node:
            raise ConfigException('%s is required' % key)
        node = node[part]


def _validate_document(value, key, fields):
    if not isinstance(value, dict):
        raise ConfigException('%s must be a dictionary' % key)
    unknown = set(value.keys()) - set(fields)
    if unknown:
        raise ConfigException('fields allowed for "%s": %s' % (key, fields))


def _validate_url(value, key):
    # TODO consider *not* validating this as both possible approaches (url
    # opening/parsing or regex match) take a big performance hit
    if value is None:
        pass
    try:
        urllib.urlopen(value)
    except IOError:
        raise ConfigException('%s does not seem to be a valid (or reachable) '
                              'url' % value)


def _validate_email(value, key):
    # TODO
    if value is None:
        pass
    pass
