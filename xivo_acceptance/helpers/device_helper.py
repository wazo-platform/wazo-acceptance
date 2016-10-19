# -*- coding: utf-8 -*-

# Copyright (C) 2013-2016 Avencall
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

import json
import requests

from lettuce.registry import world


AUTOPROV_URL = 'https://%s/xivo/configuration/json.php/restricted/provisioning/autoprov?act=configure'
HEADERS = {'Content-Type': 'application/json'}


def provision_device_using_webi(provcode, device_ip):
    auth = requests.auth.HTTPBasicAuth(world.config['rest_api']['username'],
                                       world.config['rest_api']['passwd'])
    data = json.dumps({'code': provcode, 'ip': device_ip})
    requests.post(url=AUTOPROV_URL % world.config['xivo_host'],
                  headers=HEADERS,
                  auth=auth,
                  data=data,
                  verify=False)


def add_or_replace_device(device):
    delete_similar_devices(device)
    return world.confd_client.devices.create(device)


def delete_similar_devices(device):
    if 'mac' in device:
        delete_device_with('mac', device['mac'])
    if 'ip' in device:
        delete_device_with('ip', device['ip'])


def delete_device_with(key, value):
    for device in find_devices_with(key, value):
        _delete_device(device['id'])


def find_devices_with(key, value):
    response = world.confd_client.devices.list(**{key: value})
    return response['items']


def _delete_device(device_id):
    world.confd_client.devices.autoprov(device_id)
    world.confd_client.devices.delete(device_id)
