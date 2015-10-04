Eve-Swagger
===========

Swagger extension for Eve, by `popular request`_.

TODO
----
Everything. Contributors welcome.

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
        }
    }
    app.config['SWAGGER'] = SWAGGER

    if __name__ == '__main__':
        app.run()

When API is up and running, visit the ``/api-docs`` endpoint. Please note,
right now we are serving static, incomplete, content.


.. _`popular request`: https://github.com/nicolaiarocci/eve/issues/574
