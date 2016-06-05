Eve-Swagger
===========

Swagger_ extension for Eve_ powered RESTful APIs.

Usage
-----
.. code-block:: python

    from eve import Eve
    from eve_swagger import swagger

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
    },

    # optional. Will use flask.request.host if missing.
    app.config['SWAGGER_HOST'] = 'myhost.com'

    if __name__ == '__main__':
        app.run()

When API is up and running, visit the ``/api-docs`` endpoint. The resulting
JSON can then be used with swagger tooling, like the Swagger Editor:

.. image:: resources/swagger_editor.png

Installation
------------
.. code-block::

    $ pip install eve-swagger

Copyright
---------
Cerberus is an open source project by `Nicola Iarocci`_. See the original LICENSE_ for more informations.

.. _Swagger: http://swagger.io/
.. _Eve: http://python-eve.org/
.. _`popular request`: https://github.com/nicolaiarocci/eve/issues/574
.. _LICENSE: https://github.com/nicolaiarocci/eve-swagger/blob/master/LICENSE
.. _`Nicola Iarocci`: http://nicolaiarocci.com
