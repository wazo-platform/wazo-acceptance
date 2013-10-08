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
from xivo_ws import SIPTrunk


def add_trunksip(host, name, context='default', type='friend'):
    sip_trunk = SIPTrunk()
    sip_trunk.name = name
    sip_trunk.username = sip_trunk.name
    sip_trunk.secret = sip_trunk.name
    sip_trunk.context = context
    sip_trunk.host = host
    sip_trunk.type = type
    world.ws.sip_trunks.add(sip_trunk)


def add_or_replace_trunksip(host, name, context='default', type='friend'):
    delete_trunksips_with_name(name)
    add_trunksip(host, name, context, type)


def delete_trunksips_with_name(name):
    sip_trunks = _search_trunksip_with_name(name)
    for sip_trunk in sip_trunks:
        world.ws.sip_trunks.delete(sip_trunk.id)


def find_trunksip_id_with_name(name):
    sip_trunk = _find_trunksip_with_name(name)
    return sip_trunk.id


def _find_trunksip_with_name(name):
    sip_trunks = _search_trunksip_with_name(name)
    if len(sip_trunks) != 1:
        raise Exception('expecting 1 sip trunk with name %r; found %s' %
                        (name, len(sip_trunks)))
    return sip_trunks[0]


def _search_trunksip_with_name(name):
    return world.ws.sip_trunks.search_by_name(name)
