# -*- coding: utf-8 -*-

# Copyright (C) 2013-2016 Avencall
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

from requests.exceptions import HTTPError
from lettuce import world


def add_entity(name, display_name):
    entity = get_entity_with_name(name)
    if not entity:
        body = {'name': name, 'display_name': display_name}
        world.confd_client.entities.create(body)


def get_entity_with_name(name):
    try:
        entities = world.confd_client.entities.list(name=name)['items']
        for entity in entities:
            return entity
    except HTTPError:
        return None


def default_entity_id():
    default_entity_name = world.config['default_entity']
    default_entity = get_entity_with_name(default_entity_name)
    if not default_entity:
        raise Exception('Invalid default entity {}'.format(default_entity_name))
    return default_entity['id']
