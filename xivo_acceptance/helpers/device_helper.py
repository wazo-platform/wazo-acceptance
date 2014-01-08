# -*- coding: utf-8 -*-

# Copyright (C) 2013-2014 Avencall
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

from xivo_lettuce.remote_py_cmd import remote_exec

AUTOPROV_URL = 'https://%s/xivo/configuration/json.php/restricted/provisioning/autoprov?act=configure'
HEADERS = {'Content-Type': 'application/json'}


def provision_device_using_webi(provcode, device_ip):
    data = json.dumps({'code': provcode, 'ip': device_ip})
    requests.post(url=AUTOPROV_URL % world.config.xivo_host,
                  headers=HEADERS,
                  auth=_prepare_auth(),
                  data=data,
                  verify=False)


def _prepare_auth():
    auth = requests.auth.HTTPBasicAuth(world.config.rest_username, world.config.rest_passwd)
    return auth


def create_dummy_devices(nb_devices):
    remote_exec(_create_dummy_devices, nb_devices=nb_devices)


def _create_dummy_devices(channel, nb_devices):
    from xivo_dao.data_handler.device import services as device_services
    from xivo_dao.data_handler.device.model import Device

    for i in range(nb_devices):
        device_services.create(Device())
