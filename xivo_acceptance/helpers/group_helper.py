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


def add_or_replace_group(name, exten='2000', context='default', users=None):
    delete_groups_with_name(name)
    add_group(name, exten, context, users)


def add_group(name, exten, context='default', users=None):
    group = {'name': name}
    group = world.confd_client.groups.create(group)

    extension = {'exten': exten, 'context': context}
    extension = world.confd_client.extensions.create(extension)

    world.confd_client.groups(group).add_extension(extension)

    if users:
        world.confd_client.groups(group).update_user_members(users)


def delete_groups_with_number(exten):
    extensions = world.confd_client.extensions.list(exten=exten)['items']
    for extension in extensions:
        if extension['group']:
            world.confd_client.groups.delete(extension['group']['id'])
        world.confd_client.extensions.delete(extension['id'])


def delete_groups_with_name(name):
    groups = world.confd_client.groups.list(name=name)['items']
    for group in groups:
        world.confd_client.groups.delete(group['id'])
        for extension in group['extensions']:
            world.confd_client.extensions.delete(extension['id'])


def get_group_by_name(name):
    groups = world.confd_client.groups.list(name=name)['items']
    if groups['total'] != 1:
        raise Exception('expecting 1 group with name %r; found %s' %
                        (name, groups['total']))
    return groups[0]
