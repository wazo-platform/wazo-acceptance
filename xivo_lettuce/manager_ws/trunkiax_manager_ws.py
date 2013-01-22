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
from xivo_ws import IAXTrunk


def add_trunkiax(data):
    iaxtrunk = IAXTrunk()
    iaxtrunk.name = data['name']
    iaxtrunk.context = data['context']
    world.ws.iax_trunks.add(iaxtrunk)


def add_or_replace_trunkiax(data):
    delete_trunkiaxs_with_name(data['name'])
    add_trunkiax(data)


def delete_trunkiaxs_with_name(name):
    iax_trunks = _search_trunkiax_with_name(name)
    for iax_trunk in iax_trunks:
        world.ws.iax_trunks.delete(iax_trunk.id)


def _search_trunkiax_with_name(name):
    return world.ws.iax_trunks.search_by_name(name)
