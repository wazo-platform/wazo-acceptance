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
from xivo_ws import CustomTrunk


def add_trunkcustom(data):
    customtrunk = CustomTrunk()
    customtrunk.name = data['name']
    customtrunk.interface = data['interface']
    world.ws.custom_trunks.add(customtrunk)


def add_or_replace_trunkcustom(data):
    delete_trunkcustoms_with_name(data['name'])
    add_trunkcustom(data)


def delete_trunkcustoms_with_name(name):
    custom_trunks = _search_trunkcustom_with_name(name)
    for custom_trunk in custom_trunks:
        world.ws.custom_trunks.delete(custom_trunk.id)


def find_trunkcustom_id_with_name(name):
    custom_trunk = _find_trunkcustom_with_name(name)
    return custom_trunk.id


def _find_trunkcustom_with_name(name):
    custom_trunks = _search_trunkcustom_with_name(name)
    if len(custom_trunks) != 1:
        raise Exception('expecting 1 custom trunk with name %r; found %s' %
                        (name, len(custom_trunks)))
    return custom_trunks[0]


def _search_trunkcustom_with_name(name):
    return world.ws.custom_trunks.search_by_name(name)
