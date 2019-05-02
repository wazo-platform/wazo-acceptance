# -*- coding: utf-8 -*-
# Copyright 2013-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import os


def copy_asset_to_server(context, asset, serverpath):
    assetpath = os.path.join(context.config['assets_dir'], asset)
    context.ssh_client_xivo.send_files(assetpath, serverpath)
