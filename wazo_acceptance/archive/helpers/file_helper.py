# -*- coding: utf-8 -*-
# Copyright 2013-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from lettuce import world


def create_empty_file(path):
    # if the file already exist on the fs, it will be truncated to 0
    world.ssh_client_xivo.check_call(['truncate', '-s0', path])
