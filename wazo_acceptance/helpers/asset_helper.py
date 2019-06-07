# Copyright 2013-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import os


class AssetHelper:

    def __init__(self, context):
        self._context = context
        self._ssh_client = context.ssh_client
        self._assets_dir = context.wazo_config['assets_dir']

    def copy_asset_to_server(self, asset, serverpath):
        assetpath = os.path.join(self._assets_dir, asset)
        self._ssh_client.send_files(assetpath, serverpath)
        self._context.add_cleanup(
            self._ssh_client.check_call,
            ['rm {}'.format(os.path.join(serverpath, asset))],
        )
