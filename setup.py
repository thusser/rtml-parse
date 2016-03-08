#!/usr/bin/env python

from setuptools import setup

setup(
    name='rtml-parse',
    version='0.0.1',
    packages=['rtmlparse', 'rtmlparse.elements', 'rtmlparse.templates', 'rtmlparse.tests', 'rtmlparse.examples'],
    package_data={'rtmlparse': ['schema/*.xsd']},
    description='Python package for reading/writing and manipulation of '
                'RTML (Remote Telescope Markup Language) files.',
    author='Tim-Oliver Husser',
    author_email='husser@astro.physik.uni-goettingen.de',
    url='https://github.com/thusser/rtml-parse',
    install_requires=['lxml>=2.3, <4.0', 'zope.interface', 'astropy'],
    test_suite='rtmlparse.tests'
)
