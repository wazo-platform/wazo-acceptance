# -*- coding: utf-8 -*-

# Copyright (C) 2016 Avencall
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

SIP_ENDPOINTS_URL = 'endpoints/sip'
SCCP_ENDPOINTS_URL = 'endpoints/sccp'
CUSTOM_ENDPOINTS_URL = 'endpoints/custom'


def search(search):
    return world.confd_utils_1_1.rest_get('{url}?search={search}'.format(url=SIP_ENDPOINTS_URL, search=search))


def delete(endpoint_id):
    world.confd_utils_1_1.rest_delete('{url}/{id}'.format(url=SIP_ENDPOINTS_URL, id=endpoint_id))


def create_sip(parameters=None):
    parameters = parameters or {}
    return world.confd_utils_1_1.rest_post(SIP_ENDPOINTS_URL, parameters)


def create_sccp(parameters=None):
    parameters = parameters or {}
    return world.confd_utils_1_1.rest_post(SCCP_ENDPOINTS_URL, parameters)


def create_custom(parameters=None):
    parameters = parameters or {}
    return world.confd_utils_1_1.rest_post(CUSTOM_ENDPOINTS_URL, parameters)
