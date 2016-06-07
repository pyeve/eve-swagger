#!/usr/bin/env python

from setuptools import setup, find_packages

DESCRIPTION = ("Swagger extension for Eve powered RESTful APIs")
LONG_DESCRIPTION = open('README.rst').read()

setup(
    name='Eve-Swagger',
    version='0.0.3',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author='Nicola Iarocci',
    author_email='nicola@nicolaiarocci.com',
    url='http://github.com/nicolaiarocci/cerberus',
    license=open('LICENSE').read(),
    platforms=["any"],
    packages=find_packages(),
    install_requires=['eve'],
    keywords=['swagger', 'eve', 'rest', 'api'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
)
