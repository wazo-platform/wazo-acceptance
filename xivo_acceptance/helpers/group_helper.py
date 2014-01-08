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

from lettuce import world
from xivo_ws import Group


def add_group(group_name, number='', context='default', user_ids=None):
    if not user_ids:
        user_ids = []
    group = Group()
    group.name = group_name
    group.number = number
    group.context = context
    if user_ids:
        group.user_ids = user_ids
    world.ws.groups.add(group)


def add_or_replace_group(group_name, number='', context='default', user_ids=None):
    if not user_ids:
        user_ids = []
    delete_groups_with_name(group_name)
    add_group(group_name, number, context, user_ids)


def delete_groups_with_number(group_number):
    groups = world.ws.groups.search_by_number(group_number)
    for group in groups:
        world.ws.groups.delete(group.id)


def delete_groups_with_name(group_name):
    groups = world.ws.groups.search_by_name(group_name)
    for group in groups:
        world.ws.groups.delete(group.id)


def find_group_with_name(name):
    groups = _search_groups_with_name(name)
    if len(groups) != 1:
        raise Exception('expecting 1 group with name %r; found %s' %
                        (name, len(groups)))
    return groups[0]


def find_group_id_with_name(name):
    return find_group_with_name(name).id


def get_group_with_name(name):
    group = find_group_with_name(name)
    return world.ws.groups.view(group.id)


def _search_groups_with_name(name):
    return world.ws.groups.search_by_name(name)
