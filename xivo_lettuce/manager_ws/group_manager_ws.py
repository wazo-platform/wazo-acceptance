# -*- coding: utf-8 -*-

from lettuce import world
from xivo_ws.objects.group import Group


def add_group(group_name, number='', context='default', user_ids=[]):
    group = Group()
    group.name = group_name
    group.number = number
    group.context = context
    if user_ids:
        group.user_ids = user_ids
    world.ws.groups.add(group)


def delete_group_with_number(group_number):
    groups = world.ws.groups.search_by_number(group_number)
    for group in groups:
        world.ws.groups.delete(group.id)


def delete_group_with_name(group_name):
    groups = world.ws.groups.search_by_name(group_name)
    for group in groups:
        world.ws.groups.delete(group.id)


def find_group_with_name(name):
    groups = _search_groups_with_name(name)
    if len(groups) != 1:
        raise Exception('expecting 1 group with name %r; found %s' %
                        (name, len(groups)))
    return groups[0]


def view_group_with_name(name):
    return world.ws.groups.view(find_group_with_name(name).id)


def _search_groups_with_name(name):
    return world.ws.groups.search_by_name(name)
