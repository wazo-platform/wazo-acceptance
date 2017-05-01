#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
from setuptools import find_packages


packages = find_packages(exclude=['webservices', '*.tests'])

setup(
    name='xivo-acceptance',
    version='0.1',
    description='Wazo acceptance tests',
    author='Wazo Authors',
    author_email='dev@wazo.community',
    url='http://wazo.community',
    license='GPLv3',
    packages=packages,
    scripts=[
        'bin/xivo-acceptance',
    ],
)
