# -*- coding: utf-8 -*-

from lettuce import world
from xivo_ws import CustomTrunk


def add_trunkcustom(data):
    customtrunk = CustomTrunk()
    customtrunk.name = data['name']
    customtrunk.interface = data['interface']
    world.ws.custom_trunks.add(customtrunk)


def add_or_replace_trunkcustom(data):
    delete_trunkcustom_with_name(data['name'])
    add_trunkcustom(data)


def delete_trunkcustom_with_name(name):
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
