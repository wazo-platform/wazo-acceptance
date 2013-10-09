# -*- coding: utf-8 -*-

# Copyright (C) 2013 Avencall
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

from lettuce import world
from provd.rest.client.client import new_provisioning_client

from xivo_acceptance.action.webi import provd_general as provd_general_action_webi
from xivo_lettuce.remote_py_cmd import remote_exec, remote_exec_with_result


def _provd_client():
    _, port = provd_general_action_webi.rest_api_configuration()
    provd_url = "http://%s:%s/provd" % (world.xivo_host, port)
    provd_client = new_provisioning_client(provd_url)
    return provd_client


def create_device(deviceinfo):
    remote_exec(_create_device, deviceinfo=deviceinfo)


def _create_device(channel, deviceinfo):
    import uuid
    from xivo_dao.helpers import provd_connector

    device_manager = provd_connector.device_manager()
    config_manager = provd_connector.config_manager()

    config = {
        'id': deviceinfo.get('id', str(uuid.uuid4())),
        'deletable': True,
        'parent_ids': ['base', deviceinfo.get('template_id', 'defaultconfigdevice')],
        'configdevice': deviceinfo.get('template_id', 'defaultconfigdevice'),
        'raw_config': {}
    }

    if 'template_id' in deviceinfo:
        del deviceinfo['template_id']

    deviceinfo['config'] = config['id']

    device_manager.add(deviceinfo)
    config_manager.add(config)


def get_provd_config(device_id):
    device = get_device(device_id)
    if device is None:
        raise 'device %s not exist' % device_id
    config = get_config(device['config'])
    return config


def get_config(config_id):
    config = _provd_client().config_manager().get(config_id)
    return config


def get_device(device_id):
    device = _provd_client().device_manager().get(device_id)
    return device


def total_devices():
    return remote_exec_with_result(_total_devices)


def _total_devices(channel):
    from xivo_dao.helpers import provd_connector

    device_manager = provd_connector.device_manager()
    total = len(device_manager.find())
    channel.send(total)


def device_config_has_properties(device_id, properties):
    remote_exec(_device_config_has_properties, device_id=device_id, properties=dict(properties[0]))


def _device_config_has_properties(channel, device_id, properties):
    from xivo_dao.helpers import provd_connector

    provd_config_manager = provd_connector.config_manager()
    provd_device_manager = provd_connector.device_manager()
    device = provd_device_manager.get(device_id)
    if 'config' in device:
        config = provd_config_manager.get(device['config'])

        assert 'sip_lines' in config['raw_config'], "device does not have any SIP lines configured"

        sip_lines = config['raw_config']['sip_lines']
        sip_line = sip_lines['1']

        keys = [u'username', u'auth_username', u'display_name', u'password', u'number']
        for key in keys:
            if key in properties:
                message = u"Invalid %s ('%s' instead of '%s')" % (key, sip_line[key], properties[key])
                message = message.encode('utf8')
                assert sip_line[key] == properties[key], message
    else:
        assert False, 'Device has no config key.'


def add_or_replace_device_template(properties):
    remote_exec(_add_or_replace_device_template, properties=dict(properties))


def _add_or_replace_device_template(channel, properties):
    from xivo_dao.helpers import provd_connector
    config_manager = provd_connector.config_manager()

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


def delete_device(device_id):
    remote_exec(_delete_device, device_id=device_id)


def _delete_device(channel, device_id):
    from xivo_dao.helpers import provd_connector
    config_manager = provd_connector.config_manager()
    device_manager = provd_connector.device_manager()

    try:
        config_manager.remove(device_id)
    except Exception:
        pass
    try:
        device_manager.remove(device_id)
    except Exception:
        pass


def delete_device_with_mac(mac):
    remote_exec(_delete_device_with_mac, mac=mac)


def _delete_device_with_mac(channel, mac):
    from xivo_dao.helpers import provd_connector
    config_manager = provd_connector.config_manager()
    device_manager = provd_connector.device_manager()

    for device in device_manager.find({'mac': mac}):
        try:
            config_manager.remove(device['id'])
        except Exception:
            pass
        device_manager.remove(device['id'])


def delete_device_with_ip(ip):
    remote_exec(_delete_device_with_ip, ip=ip)


def _delete_device_with_ip(channel, ip):
    from xivo_dao.helpers import provd_connector
    config_manager = provd_connector.config_manager()
    device_manager = provd_connector.device_manager()

    for device in device_manager.find({'ip': ip}):
        try:
            config_manager.remove(device['id'])
        except Exception:
            pass
        device_manager.remove(device['id'])


def delete_all():
    remote_exec(_delete_all)


def _delete_all(channel):
    from xivo_dao.helpers import provd_connector
    config_manager = provd_connector.config_manager()
    device_manager = provd_connector.device_manager()

    for device in device_manager.find():
        try:
            config_manager.remove(device['id'])
        except Exception:
            pass
        device_manager.remove(device['id'])


def remove_devices_over(max_devices):
    remote_exec(_remove_devices_over, max_devices=max_devices)


def _remove_devices_over(channel, max_devices):
    from xivo_dao.helpers import provd_connector
    config_manager = provd_connector.config_manager()
    device_manager = provd_connector.device_manager()

    all_devices = device_manager.find()
    extra_devices = all_devices[max_devices:]

    for device in extra_devices:
        device_manager.remove(device['id'])
        if 'config' in device:
            config_manager.remove(device['config'])


def find_by_mac(mac):
    return remote_exec_with_result(_find_by_mac, mac=mac)


def _find_by_mac(channel, mac):
    from xivo_dao.helpers import provd_connector
    device_manager = provd_connector.device_manager()

    devices = device_manager.find({'mac': mac})
    if len(devices) == 0:
        channel.send(None)
    else:
        channel.send(devices[0])
