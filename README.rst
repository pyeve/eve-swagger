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


    if __name__ == '__main__':
        app.run()

When API is up and running, visit the ``/api-docs`` endpoint. Please note,
right now we are serving static, incomplete, content.


.. _`popular request`: https://github.com/nicolaiarocci/eve/issues/574
