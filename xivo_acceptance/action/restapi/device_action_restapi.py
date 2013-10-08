# -*- coding: utf-8 -*-
#
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

from lettuce.registry import world


DEVICES_URL = 'devices'


def create_device(parameters):
    return world.restapi_utils_1_1.rest_post(DEVICES_URL, parameters)


def synchronize(device_id):
    return world.restapi_utils_1_1.rest_get('%s/%s/synchronize' % (DEVICES_URL, device_id))


def delete_device(device_id):
    return world.restapi_utils_1_1.rest_delete("%s/%s" % (DEVICES_URL, device_id))


def get_device(device_id):
    return world.restapi_utils_1_1.rest_get("%s/%s" % (DEVICES_URL, device_id))


def device_list(parameters={}):
    return world.restapi_utils_1_1.rest_get(DEVICES_URL, params=parameters)


def reset_to_autoprov(device_id):
    return world.restapi_utils_1_1.rest_get('%s/%s/autoprov' % (DEVICES_URL, device_id))


def associate_line_to_device(device_id, line_id):
    return world.restapi_utils_1_1.rest_get('%s/%s/associate_line/%s' % (DEVICES_URL, device_id, line_id))


def remove_line_from_device(device_id, line_id):
    return world.restapi_utils_1_1.rest_get('%s/%s/remove_line/%s' % (DEVICES_URL, device_id, line_id))


def edit_device(device_id, parameters):
    return world.restapi_utils_1_1.rest_put("%s/%s" % (DEVICES_URL, device_id), parameters)
