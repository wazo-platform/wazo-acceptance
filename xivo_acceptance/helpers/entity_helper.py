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

from __future__ import unicode_literals

from lettuce import world

from xivo_ws.objects.entity import Entity
from xivo_lettuce import postgres


def add_entity(name, display_name):
    entity = get_entity_with_name(name)
    if not entity:
        entity = Entity(name=name, display_name=display_name)
        world.ws.entities.add(entity)


def get_entity_with_name(name):
    query = 'SELECT * FROM "entity" WHERE name = \'%s\';' % name
    result = postgres.exec_sql_request(query).fetchone()
    if result:
        return result
    return None


def oldest_entity_id():
    """The closest we have to the "default" entity"""
    query = 'SELECT id FROM "entity" ORDER BY "id"'
    result = postgres.exec_sql_request(query).fetchone()
    return result.id
