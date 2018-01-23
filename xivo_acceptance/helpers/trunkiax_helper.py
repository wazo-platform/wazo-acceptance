# -*- coding: utf-8 -*-

# Copyright 2013-2018 The Wazo Authors  (see the AUTHORS file)
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


def add_trunkiax(name, context='default'):
    endpoint = world.confd_client.endpoints_iax.create({'name': name})
    trunk = world.confd_client.trunks.create({'context': context})
    world.confd_client.trunks(trunk).add_endpoint_iax(endpoint)


def add_or_replace_trunkiax(name, context='default'):
    delete_trunkiaxs_with_name(name)
    add_trunkiax(name, context)


def delete_trunkiaxs_with_name(name):
    endpoints = world.confd_client.endpoints_iax.list(name=name)['items']
    for endpoint in endpoints:
        world.confd_client.endpoints_iax.delete(endpoint)
        if endpoint['trunk']:
            world.confd_client.trunks.delete(endpoint['trunk']['id'])
