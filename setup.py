#!/usr/bin/env python
"""
Setup for Swagger extension for Eve powered RESTful APIs
"""
from os.path import abspath, dirname, join
from shlex import split
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand  # noqa N812


def read_file(filename):
    """Read the contents of a file located relative to setup.py"""
    with open(join(abspath(dirname(__file__)), filename)) as thefile:
        return thefile.read()


class Tox(TestCommand):
    """Integration of tox via the setuptools ``test`` command"""
    # pylint: disable=attribute-defined-outside-init
    user_options = [('tox-args=', 'a', "Arguments to pass to tox")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.tox_args = None

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        from tox import cmdline  # pylint: disable=import-error
        args = self.tox_args
        if args:
            args = split(self.tox_args)
        cmdline(args=args)


setup(
    name='Eve-Swagger',
    version='0.0.11',
    description='Swagger extension for Eve powered RESTful APIs',
    long_description=read_file('README.rst'),
    author='Nicola Iarocci',
    author_email='nicola@nicolaiarocci.com',
    url='http://github.com/pyeve/eve-swagger',
    license='BSD',
    platforms=["any"],
    packages=find_packages(),
    install_requires=read_file('requirements.txt'),
    keywords=['swagger', 'eve', 'rest', 'api'],
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
    tests_require=['tox'],
    cmdclass={
        'test': Tox,
    },
)
