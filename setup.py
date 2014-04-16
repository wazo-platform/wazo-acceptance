#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from distutils.core import setup

setup(
    name='xivo-acceptance',
    version='0.1',
    description='XiVO Acceptance',
    author='Avencall',
    author_email='dev@avencall.com',
    url='https://github.com/xivo-pbx/xivo-acceptance',
    license='GPLv3',
    packages=['xivo_acceptance', 'xivo_lettuce'],
    data_files=[('/etc/xivo-acceptance', ['config/default.ini',
                                          'config/conf.d/default',
                                          'config/conf.d/daily-xivo-pxe',
                                          'config/conf.d/daily-xivo-script',
                                          'config/conf.d/daily-xivo-upgraded',
                                          'config/conf.d/daily-xivo-vanilla']),
                ('/usr/share/xivo-acceptance/assets', ['assets/ca-certificates.crt',
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
