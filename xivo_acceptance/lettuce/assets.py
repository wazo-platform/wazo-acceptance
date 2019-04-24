# -*- coding: utf-8 -*-
# Copyright 2013-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import os
from lettuce import world


def copy_asset_to_server(asset, serverpath):
    assetpath = os.path.join(world.config['assets_dir'], asset)
    world.ssh_client_xivo.send_files(assetpath, serverpath)
