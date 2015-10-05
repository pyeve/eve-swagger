Eve-Swagger
===========

Swagger_ extension for Eve, by `popular request`_.

Current Status
--------------
Experimental playground.


Usage
-----
.. code-block:: python

    from eve import Eve
    from eve_swagger import swagger

    app = Eve()
    app.register_blueprint(swagger)

    # You might want to simply update the eve settings module instead.
    SWAGGER = {
        'info': {
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
        'host': 'myhost.com'
    }
    app.config['SWAGGER'] = SWAGGER

    if __name__ == '__main__':
        app.run()

When API is up and running, visit the ``/api-docs`` endpoint. The resulting
JSON can then be used with swagger tooling, like the Swagger Editor:

.. image:: resources/swagger_editor.png


.. _Swagger: http://swagger.io/
.. _`popular request`: https://github.com/nicolaiarocci/eve/issues/574
