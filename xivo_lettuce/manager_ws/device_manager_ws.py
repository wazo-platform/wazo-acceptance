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


def find_device_id_with_mac(mac):
    return find_device_with_mac(mac).id


def find_device_with_mac(mac):
    devices = _search_devices_with_mac(mac)
    if len(devices) != 1:
        raise Exception('expecting 1 device with mac %s' % mac)
    return devices[0]


def _search_devices_with_mac(mac):
    return [d for d in world.ws.devices.list() if d.mac == mac]
