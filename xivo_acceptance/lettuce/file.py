# -*- coding: utf-8 -*-
# Copyright (C) 2013-2014 Avencall
# SPDX-License-Identifier: GPL-3.0-or-later

import errno
import os
from lettuce import world


def remove_in_download_dir(filename):
    path = os.path.join(world.browser.DOWNLOAD_DIR, filename)
    try:
        os.remove(path)
    except OSError as e:
        if e.errno != errno.ENOENT:
            raise


def isfile_in_download_dir(filename):
    path = os.path.join(world.browser.DOWNLOAD_DIR, filename)
    return os.path.isfile(path)
