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

# TODO since in swagger 'additional properties not allowed', we also
# need to validate that there are not unknown fields in every (sub)document.
# Or maybe have a relaxed approach to validation, and just ignore the issue
# since swagger tooling will report the error anyway.


def validate_info():
    _validate_required('info')

    info = app.config[eve_swagger.SWAGGER].get('info')

    _validate_required('info.title')
    _validate_required('info.version')

    def validate_contact():
        contact = info.get('contact')
        if contact is None:
            return
        _validate_document(contact, 'info.contact')
        _validate_url(contact.get('url'), 'info.contact.url')

    def validate_license():
        license = info.get('license')
        if license is None:
            return
        _validate_document(license, 'info.license')
        _validate_required('info.license.name')
        _validate_url(license.get('url'), 'info.license.url')
        _validate_email(license.get('email'), 'info.license.email')

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


def _validate_document(value, key):
    if not isinstance(value, dict):
        raise ConfigException('%s must be a dictionary' % key)


def _validate_url(value, key):
    # TODO
    if value:
        pass
    pass


def _validate_email(value, key):
    # TODO
    if value:
        pass
    pass
