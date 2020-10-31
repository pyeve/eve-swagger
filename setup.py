#!/usr/bin/env python
"""
Setup for Swagger extension for Eve powered RESTful APIs
"""
from setuptools import setup, find_packages
from collections import OrderedDict

DESCRIPTION = "Swagger extension for Eve powered RESTful APIs"
with open("README.rst") as f:
    LONG_DESCRIPTION = f.read()

INSTALL_REQUIRES = ["eve"]

EXTRAS_REQUIRES = {
    "docs": [],
    "tests": ["pytest", "tox", "jsonschema", "pyrsistent<=0.16"],
}
EXTRAS_REQUIRES["dev"] = EXTRAS_REQUIRES["tests"] + EXTRAS_REQUIRES["docs"]

setup(
    name="Eve-Swagger",
    version="0.1.2",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author="Nicola Iarocci",
    author_email="nicola@nicolaiarocci.com",
    url="http://github.com/pyeve/eve-swagger",
    project_urls=OrderedDict(
        (
            ("Documentation", "http://python-eve.org"),
            ("Code", "https://github.com/pyeve/eve-swagger"),
            ("Issue tracker", "https://github.com/pyeve/eve-swagger/issues"),
        )
    ),
    license="BSD",
    platforms=["any"],
    packages=find_packages(),
    install_requires=INSTALL_REQUIRES,
    extras_require=EXTRAS_REQUIRES,
    include_package_data=True,
    test_suite="eve_swagger.tests",
    keywords=["swagger", "eve", "rest", "api"],
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
)
