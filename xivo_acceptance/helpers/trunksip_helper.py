# -*- coding: utf-8 -*-

# Copyright (C) 2013-2014 Avencall
# Copyright (C) 2016 Proformatique Inc.
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


def add_trunksip(host, name, context='default', type='friend'):
    body = {'username': name,
            'secret': name,
            'host': host,
            'type': type}
    endpoint_sip = world.confd_client.endpoints_sip.create(body)

    body = {'context': context}
    trunk = world.confd_client.trunks.create(body)

    world.confd_client.trunks(trunk).add_endpoint_sip(endpoint_sip)


def add_or_replace_trunksip(host, name, context='default', type='friend'):
    delete_trunksips_with_name(name)
    add_trunksip(host, name, context, type)


def delete_trunksips_with_name(name):
    endpoints_sip = world.confd_client.endpoints_sip.list(username=name)['items']
    for endpoint_sip in endpoints_sip:
        if endpoint_sip['trunk']:
            world.confd_client.trunks.delete(endpoint_sip['trunk']['id'])


def find_trunksip_id_with_name(name):
    endpoints_sip = world.confd_client.endpoints_sip.list(username=name)['items']
    if len(endpoints_sip) != 1:
        raise Exception('expecting 1 sip trunk with name %r; found %s' %
                        (name, len(endpoints_sip)))
    return endpoints_sip[0]['trunk']['id']
