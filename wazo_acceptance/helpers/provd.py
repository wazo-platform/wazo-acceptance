# Copyright 2013-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import requests
from hamcrest import (
    assert_that,
    is_,
)

from wazo_provd_client import operation
from wazo_provd_client.exceptions import ProvdError
from wazo_test_helpers import until


class Provd:

    def __init__(self, context):
        self._context = context
        self._provd_client = context.provd_client

    def _operation_successful(self, operation_ressource):
        operation_ressource.update()
        assert_that(operation_ressource.state, is_(operation.OIP_SUCCESS))

    def get_config(self, id_):
        return self._context.provd_client.configs.get(id_)

    def update_plugin_list(self, url):
        self._provd_client.params.update('plugin_server', url)
        with self._provd_client.plugins.update() as operation_progress:
            until.assert_(
                self._operation_successful, operation_progress, tries=20, interval=0.5
            )

    def get_latest_plugin_name(self, plugin_name):
        all_plugins = self._provd_client.plugins.list_installable()['pkgs']
        matching_plugins = [plugin for plugin in all_plugins if plugin_name in plugin]
        if not matching_plugins:
            raise Exception(f'no matching plugins for {plugin_name}')
        return max(matching_plugins)

    def install_latest_plugin(self, plugin):
        latest_plugin = self.get_latest_plugin_name(plugin)
        plugins_installed = self._provd_client.plugins.list_installed()['pkgs']
        if latest_plugin not in plugins_installed:
            self.install_plugin(latest_plugin)

    def install_plugin(self, plugin_name):
        with self._provd_client.plugins.install(plugin_name) as operation_progress:
            until.assert_(
                self._operation_successful, operation_progress, tries=20, interval=0.5
            )

    def create_device_via_http_request(self, path, user_agent, mac=None):
        host = self._context.wazo_config['wazo_host']
        url = f'http://{host}:8667/{path}'
        requests.get(url, headers={'User-Agent': user_agent})
        if mac:
            self._context.add_cleanup(self.delete_device_with_mac, mac)

    def delete_device(self, device_id):
        devices = self._provd_client.devices.list({'id': device_id})['devices']
        device = devices[0] if devices else None
        if not device:
            return

        config_id = device.get('config', device['id'])
        configs = self._provd_client.configs.list({'id': config_id})['configs']
        config = configs[0] if configs else None

        self._provd_client.devices.delete(device['id'])
        if config:
            try:
                self._provd_client.configs.delete(config['id'])
            except ProvdError:
                pass

    def delete_device_with_mac(self, mac):
        device = self._find_by('mac', mac)
        if device:
            self.delete_device(device['id'])

    def _find_by(self, key, value):
        devices = self._provd_client.devices.list({key: value})['devices']
        return devices[0] if devices else None
