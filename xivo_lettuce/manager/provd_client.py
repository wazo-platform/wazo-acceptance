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
from xivo_lettuce.manager import provd_general_manager


def delete_device_by_mac(mac_address):
    provd_url = _provd_url()
    provd_client = new_provisioning_client(provd_url)
    devices = provd_client.device_manager().find({'mac': mac_address})
    for device in devices:
        if 'config' in device:
            provd_client.config_manager().remove(device['config'])
        provd_client.device_manager().remove(device['id'])


def create_device(mac_address, plugin):
    provd_url = _provd_url()
    provd_client = new_provisioning_client(provd_url)
    device_add_request = {
        'mac': mac_address,
        'plugin': plugin,
    }
    new_device_id = provd_client.device_manager().add(device_add_request)
    new_config_id = provd_client.config_manager().autocreate()
    new_device = provd_client.device_manager().get(new_device_id)
    new_device['config'] = new_config_id
    provd_client.device_manager().update(new_device)


def get_config(config_id):
    provd_url = _provd_url()
    provd_client = new_provisioning_client(provd_url)
    config = provd_client.config_manager().get(config_id)
    return config


def _provd_url():
    _, port = provd_general_manager.rest_api_configuration()
    url = "http://%s:%s/provd" % (world.xivo_host, port)
    return url
