# -*- coding: utf-8 -*-
"""
    eve-swagger
    ~~~~~~~~~~~
    swagger.io extension for Eve-powered REST APIs.

    :copyright: (c) 2015 by Nicola Iarocci.
    :license: BSD, see LICENSE for more details.
"""
try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict  # noqa: F401
from .swagger import swagger, add_documentation  # noqa

INFO = "SWAGGER_INFO"
HOST = "SWAGGER_HOST"
