# -*- coding: utf-8 -*-
# Copyright 2013-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import urllib2
from lettuce import world
from hamcrest import assert_that, is_not, none, has_entry, has_entries, has_key, is_
from xivo_test_helpers import until
from wazo_provd_client.exceptions import ProvdError
from wazo_provd_client import operation
import uuid


def device_config_has_properties(device_id, properties):
    config = get_provd_config(device_id)
    assert_that(config, has_entry('raw_config', has_entry('sip_lines', has_entry('1', has_entries(properties)))))


def get_provd_config(device_id):
    device = _check_device_exists(device_id)
    config = _check_device_has_config(device)
    return config


def _check_device_exists(device_id):
    device = world.provd_client.devices.get(device_id)
    assert_that(device, is_not(none()), "Device id %s does not exist" % device_id)
    return device


def _check_device_has_config(device):
    assert_that(device, has_key('config'), "Device does not have config key")

    config = world.provd_client.configs.get(device['config'])
    assert_that(config, is_not(none()), "Config %s does not exist" % device['config'])

    return config


def total_devices():
    device_manager = world.provd_client.devices
    return len(device_manager.list()['devices'])


def get_device(device_id):
    return world.provd_client.devices.get(device_id)


def create_device(deviceinfo):
    deviceinfo = dict(deviceinfo)
    device_manager = world.provd_client.devices
    config_manager = world.provd_client.configs

    device_id = deviceinfo.get('id', uuid.uuid4().hex)
    template_id = deviceinfo.pop('template_id', 'defaultconfigdevice')

    config = {
        'id': device_id,
        'deletable': True,
        'parent_ids': ['base', template_id],
        'configdevice': template_id,
        'raw_config': {}
    }

    device_manager.create(deviceinfo)
    config_manager.create(config)


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


def delete_device_with_ip(ip):
    device = _find_by('ip', ip)
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
