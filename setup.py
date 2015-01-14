#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import fnmatch
import os

from setuptools import setup
from setuptools import find_packages


def data(source_dir, dest_dir):
    for root, dirnames, filenames in os.walk(source_dir):
        relpath = os.path.relpath(root, source_dir)
        newpath = os.path.join(dest_dir, relpath)
        yield (newpath, [os.path.join(root, filename) for filename in filenames])

setup(
    name='xivo-acceptance',
    version='0.1',
    description='XiVO Acceptance',
    author='Avencall',
    author_email='dev@avencall.com',
    url='https://github.com/xivo-pbx/xivo-acceptance',
    license='GPLv3',
    packages=find_packages(),
    scripts=[
        'bin/xivo-acceptance',
    ],
    data_files=list(
        data('data', 'share/xivo-acceptance')
    )
)
