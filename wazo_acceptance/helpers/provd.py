# Copyright 2013-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import requests
from hamcrest import (
    assert_that,
    is_,
)

from wazo_provd_client import operation
from wazo_provd_client.exceptions import ProvdError
from xivo_test_helpers import until


class Provd:

    def __init__(self, context):
        self._context = context

    def _operation_successful(self, operation_ressource):
        operation_ressource.update()
        assert_that(operation_ressource.state, is_(operation.OIP_SUCCESS))

    def update_plugin_list(self, url):
        self._context.provd_client.params.update('plugin_server', url)
        with self._context.provd_client.plugins.update() as operation_progress:
            until.assert_(
                self._operation_successful, operation_progress, tries=20, interval=0.5
            )

    def get_latest_plugin_name(self, plugin_name):
        all_plugins = self._context.provd_client.plugins.list_installable()['pkgs']
        matching_plugins = [plugin for plugin in all_plugins if plugin_name in plugin]
        if not matching_plugins:
            raise Exception('no matching plugins for {}'.format(plugin_name))
        return max(matching_plugins)

    def install_latest_plugin(self, plugin):
        latest_plugin = self.get_latest_plugin_name(plugin)
        plugins_installed = self._context.provd_client.plugins.list_installed()['pkgs']
        if latest_plugin not in plugins_installed:
            self.install_plugin(latest_plugin)

    def install_plugin(self, plugin_name):
        with self._context.provd_client.plugins.install(plugin_name) as operation_progress:
            until.assert_(
                self._operation_successful, operation_progress, tries=20, interval=0.5
            )

    def request_http(self, path, user_agent):
        url = 'http://{}:8667/{}'.format(self._context.wazo_config['wazo_host'], path)
        requests.get(url, headers={'User-Agent': user_agent})

    def delete_device(self, device_id):
        device_manager = self._context.provd_client.devices
        config_manager = self._context.provd_client.configs

        devices = device_manager.list({'id': device_id})['devices']
        device = devices[0] if devices else None
        if not device:
            return

        config_id = device.get('config', device['id'])
        configs = config_manager.list({'id': config_id})['configs']
        config = configs[0] if configs else None

        device_manager.delete(device['id'])
        if config:
            try:
                config_manager.delete(config['id'])
            except ProvdError:
                pass

    def delete_device_with_mac(self, mac):
        device = self._find_by('mac', mac)
        if device:
            self.delete_device(device['id'])

    def _find_by(self, key, value):
        device_manager = self._context.provd_client.devices
        devices = device_manager.list({key: value})['devices']
        return devices[0] if devices else None
