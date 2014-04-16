#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import fnmatch
import os

from distutils.core import setup


def is_package(path):
    is_svn_dir = fnmatch.fnmatch(path, '*/.svn*')
    is_test_module = fnmatch.fnmatch(path, '*tests')
    return not (is_svn_dir or is_test_module)


def packages_in(package):
    return [p for p, _, _ in os.walk(package) if is_package(p)]


packages = (packages_in('xivo_acceptance') +
            packages_in('xivo_lettuce') +
            packages_in('xivo_steps'))

setup(
    name='xivo-acceptance',
    version='0.1',
    description='XiVO Acceptance',
    author='Avencall',
    author_email='dev@avencall.com',
    url='https://github.com/xivo-pbx/xivo-acceptance',
    license='GPLv3',
    packages=packages,
    data_files=[('config', ['config/default.ini',
                            'config/conf.d/default',
                            'config/conf.d/daily-xivo-pxe',
                            'config/conf.d/daily-xivo-script',
                            'config/conf.d/daily-xivo-upgraded',
                            'config/conf.d/daily-xivo-vanilla']),
                ('assets', ['assets/ca-certificates.crt',
                            'assets/cel-extract.sql',
                            'assets/core_dump',
                            'assets/core_dump.c',
                            'assets/phonebook-dbvars.csv',
                            'assets/phonebook-unicode.csv',
                            'assets/phonebook-x254.csv',
                            'assets/phonebook-x268.csv',
                            'assets/test-variable.ui',
                            'assets/xivo-backup-manager'])],
)
