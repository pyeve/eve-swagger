Eve-Swagger |latest-version|
============================

|build-status| |python-support| 

Swagger_ extension for Eve_ powered RESTful APIs.

Usage
-----
.. code-block:: python

    from eve import Eve
    from eve_swagger import swagger, add_documentation

    app = Eve()
    app.register_blueprint(swagger)

    # required. See http://swagger.io/specification/#infoObject for details.
    app.config['SWAGGER_INFO'] = {
        'title': 'My Supercool API',
        'version': '1.0',
        'description': 'an API description',
        'termsOfService': 'my terms of service',
        'contact': {
            'name': 'nicola',
            'url': 'http://nicolaiarocci.com'
        },
        'license': {
            'name': 'BSD',
            'url': 'https://github.com/nicolaiarocci/eve-swagger/blob/master/LICENSE',
        }
    }

    # optional. Will use flask.request.host if missing.
    app.config['SWAGGER_HOST'] = 'myhost.com'

    # optional. Add/Update elements in the documentation at run-time without deleting subtrees.
    add_documentation({'paths': {'/status': {'get': {'parameters': [
        {
            'in': 'query',
            'name': 'foobar',
            'required': False,
            'description': 'special query parameter',
            'type': 'string'
        }]
    }}}})

    if __name__ == '__main__':
        app.run()

When API is up and running, visit the ``/api-docs`` endpoint. The resulting
JSON can then be used with swagger tooling, like the Swagger Editor:

.. image:: resources/swagger_editor.png

Installation
------------
.. code-block::

    $ pip install eve-swagger


Description fields on the swagger docs
--------------------------------------

If you would like to include description fields to your swagger docs you can
include a description field in your schema validations in your `settings.py`

As an example:

.. code-block:: python

   ...
    'userName': {
        'description': 'The username of the logged in user.',
        'type': 'string',
        'minlength': 1,
        'maxlength': 256,
        'required': True
    },
    ...
    
**NOTE**: If you do use that feature make sure that the `TRANSPARENT_SCHEMA_RULES`
in your `settings.py` is also turned ON, otherwise you will get complains from the
Cerberus library about "unknown field 'description' for field [yourFieldName]"

Copyright
---------
Eve-Swagger is an open source project by `Nicola Iarocci`_.
See the original LICENSE_ for more informations.

.. |latest-version| image:: https://img.shields.io/pypi/v/eve-swagger.svg
   :alt: Latest version on PyPI
   :target: https://pypi.python.org/pypi/eve-swagger
.. |build-status| image:: https://travis-ci.org/nicolaiarocci/eve-swagger.svg?branch=master
   :alt: Build status
   :target: https://travis-ci.org/nicolaiarocci/eve-swagger
.. |python-support| image:: https://img.shields.io/pypi/pyversions/eve-swagger.svg
   :target: https://pypi.python.org/pypi/eve-swagger
   :alt: Python versions
.. |license| image:: https://img.shields.io/pypi/l/eve-swagger.svg
   :alt: Software license
   :target: https://github.com/nicolaiarocci/eve-swagger/blob/master/LICENSE

.. _Swagger: http://swagger.io/
.. _Eve: http://python-eve.org/
.. _`popular request`: https://github.com/nicolaiarocci/eve/issues/574
.. _LICENSE: https://github.com/nicolaiarocci/eve-swagger/blob/master/LICENSE
.. _`Nicola Iarocci`: http://nicolaiarocci.com
