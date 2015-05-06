# -*- coding: utf-8 -*-

# Copyright (C) 2013-2015 Avencall
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

import urllib2
from lettuce import world
from hamcrest import assert_that, is_not, none, has_entry, has_entries, has_key
from xivo_provd_client.error import NotFoundError
import uuid


def device_config_has_properties(device_id, properties):
    config = get_provd_config(device_id)
    assert_that(config, has_entry('raw_config', has_entry('sip_lines', has_entry('1', has_entries(properties)))))


def get_provd_config(device_id):
    device = _check_device_exists(device_id)
    config = _check_device_has_config(device)
    return config


def _check_device_exists(device_id):
    device = world.provd_client.device_manager().get(device_id)
    assert_that(device, is_not(none()), "Device id %s does not exist" % device_id)
    return device


def _check_device_has_config(device):
    assert_that(device, has_key('config'), "Device does not have config key")

    config = world.provd_client.config_manager().get(device['config'])
    assert_that(config, is_not(none()), "Config %s does not exist" % device['config'])

    return config


def add_or_replace_device_template(properties):
    config_manager = world.provd_client.config_manager()

    if 'id' in properties:
        existing = config_manager.find({'X_type': 'device', 'id': properties['id']})
        if len(existing) > 0:
            return

    default_properties = {
        'X_type': 'device',
        'deletable': True,
        'parent_ids': [],
        'raw_config': {}
    }

    properties.update(default_properties)

    config_manager.add(properties)


def total_devices():
    device_manager = world.provd_client.device_manager()
    return len(device_manager.find())


def get_device(device_id):
    return world.provd_client.device_manager().get(device_id)


def create_device(deviceinfo):
    deviceinfo = dict(deviceinfo)
    device_manager = world.provd_client.device_manager()
    config_manager = world.provd_client.config_manager()

    device_id = deviceinfo.get('id', uuid.uuid4().hex)
    template_id = deviceinfo.pop('template_id', 'defaultconfigdevice')

    config = {
        'id': device_id,
        'deletable': True,
        'parent_ids': ['base', template_id],
        'configdevice': template_id,
        'raw_config': {}
    }

    device_manager.add(deviceinfo)
    config_manager.add(config)


def find_by_mac(mac):
    return _find_by('mac', mac)


def get_by_mac(mac):
    device = find_by_mac(mac)
    assert_that(device, is_not(none()), "Device %s does not exist" % mac)
    return device


def delete_device(device_id):
    device_manager = world.provd_client.device_manager()
    config_manager = world.provd_client.config_manager()

    devices = device_manager.find({'id': device_id})
    device = devices[0] if devices else None
    if not device:
        return

    config_id = device.get('config', device['id'])
    configs = config_manager.find({'id': config_id})
    config = configs[0] if configs else None

    device_manager.remove(device['id'])
    if config:
        try:
            config_manager.remove(config['id'])
        except NotFoundError:
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
    device_manager = world.provd_client.device_manager()
    devices = device_manager.find({key: value})
    return devices[0] if devices else None


def request_http(path, user_agent):
    url = 'http://%s:8667/%s' % (world.config['xivo_host'], path)
    request = urllib2.Request(url, headers={'User-Agent': user_agent})
    fobj = urllib2.urlopen(request)
    try:
        fobj.read()
    finally:
        fobj.close()
