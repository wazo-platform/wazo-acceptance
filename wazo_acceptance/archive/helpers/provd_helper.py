# -*- coding: utf-8 -*-
# Copyright 2013-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import urllib2
from lettuce import world
from hamcrest import assert_that, is_not, none, is_
from xivo_test_helpers import until
from wazo_provd_client.exceptions import ProvdError
from wazo_provd_client import operation


def find_by_mac(mac):
    return _find_by('mac', mac)


def get_by_mac(mac):
    device = find_by_mac(mac)
    assert_that(device, is_not(none()), "Device %s does not exist" % mac)
    return device


def delete_device(device_id):
    device_manager = world.provd_client.devices
    config_manager = world.provd_client.configs

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


def delete_device_with_mac(mac):
    device = _find_by('mac', mac)
    if device:
        delete_device(device['id'])


def _find_by(key, value):
    device_manager = world.provd_client.devices
    devices = device_manager.list({key: value})['devices']
    return devices[0] if devices else None


def update_plugin_list(url):
    world.provd_client.params.update('plugin_server', url)
    with world.provd_client.plugins.update() as operation_progress:
        until.assert_(
            operation_successful, operation_progress, tries=20, interval=0.5
        )


def get_latest_plugin_name(plugin_name):
    all_plugins = world.provd_client.plugins.list_installable()['pkgs']
    matching_plugins = [plugin for plugin in all_plugins if plugin_name in plugin]
    if not matching_plugins:
        raise Exception('no matching plugins for {}'.format(plugin_name))
    return max(matching_plugins)


def install_latest_plugin(plugin):
    latest_plugin = get_latest_plugin_name(plugin)
    plugins_installed = world.provd_client.plugins.list_installed()['pkgs']
    if latest_plugin not in plugins_installed:
        install_plugin(latest_plugin)


def install_plugin(plugin_name):
    with world.provd_client.plugins.install(plugin_name) as operation_progress:
        until.assert_(
            operation_successful, operation_progress, tries=20, interval=0.5
        )


def plugins_successfully_updated():
    with world.provd_client.plugins.update() as operation_progress:
        until.assert_(
            operation_successful, operation_progress, tries=20, interval=0.5
        )


def operation_successful(operation_ressource):
    operation_ressource.update()
    assert_that(operation_ressource.state, is_(operation.OIP_SUCCESS))


def request_http(path, user_agent):
    url = 'http://%s:8667/%s' % (world.config['xivo_host'], path)
    request = urllib2.Request(url, headers={'User-Agent': user_agent})
    fobj = urllib2.urlopen(request)
    try:
        fobj.read()
    finally:
        fobj.close()
