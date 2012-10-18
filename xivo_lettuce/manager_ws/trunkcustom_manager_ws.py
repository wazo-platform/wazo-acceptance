# -*- coding: utf-8 -*-

from lettuce import world
from xivo_ws import CustomTrunk


def get_trunkcustom_id_with_name(name):
    customtrunks = world.ws.custom_trunks.list()
    for customtrunk in customtrunks:
        if customtrunk.name == str(name):
            return customtrunk.id
    raise Exception('no trunkcustom with name %s' % name)


def add_customtrunk(data):
    customtrunk = CustomTrunk()
    customtrunk.name = data['name']
    customtrunk.interface = data['interface']
    world.ws.custom_trunks.add(customtrunk)


def add_or_replace_customtrunk(data):
    delete_customtrunk_with_name_if_exists(data['name'])
    add_customtrunk(data)


def find_customtrunk_id_with_name(name):
    customtrunks = world.ws.custom_trunks.list()
    if customtrunks:
        return [customtrunk.id for customtrunk in customtrunks if
                customtrunk.name == str(name)]
    return []


def delete_customtrunk_with_id(trunk_id):
    world.ws.custom_trunks.delete(trunk_id)


def delete_customtrunk_with_name_if_exists(name):
    try:
        customtrunk_id = get_trunkcustom_id_with_name(name)
    except Exception:
        pass
    else:
        delete_customtrunk_with_id(customtrunk_id)
