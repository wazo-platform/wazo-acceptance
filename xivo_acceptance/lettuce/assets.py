# -*- coding: utf-8 -*-
# Copyright (C) 2013-2014 Avencall
# SPDX-License-Identifier: GPL-3.0-or-later

import os
from lettuce import world


def copy_asset_to_server(asset, serverpath):
    assetpath = os.path.join(world.config['assets_dir'], asset)
    world.ssh_client_xivo.send_files(assetpath, serverpath)


def full_path(asset):
    return os.path.join(world.config['assets_dir'], asset)
