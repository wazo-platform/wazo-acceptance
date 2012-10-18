# -*- coding: utf-8 -*-

from lettuce import world
from xivo_ws import IAXTrunk


def get_trunkiax_id_with_name(name):
    iaxtrunks = world.ws.iax_trunks.list()
    for iaxtrunk in iaxtrunks:
        if iaxtrunk.name == str(name):
            return iaxtrunk.id
    raise Exception('no trunkiax with name %s' % name)


def add_iaxtrunk(data):
    iaxtrunk = IAXTrunk()
    iaxtrunk.name = data['name']
    iaxtrunk.context = data['context']
    world.ws.iax_trunks.add(iaxtrunk)


def add_or_replace_iaxtrunk(data):
    delete_iaxtrunk_with_name_if_exists(data['name'])
    add_iaxtrunk(data)


def find_iaxtrunk_id_with_name(name):
    iaxtrunks = world.ws.iax_trunks.list()
    if iaxtrunks:
        return [iaxtrunk.id for iaxtrunk in iaxtrunks if
                iaxtrunk.name == str(name)]
    return []


def delete_iaxtrunk_with_id(trunk_id):
    world.ws.iax_trunks.delete(trunk_id)


def delete_iaxtrunk_with_name_if_exists(name):
    try:
        iaxtrunk_id = get_trunkiax_id_with_name(name)
    except Exception:
        pass
    else:
        delete_iaxtrunk_with_id(iaxtrunk_id)
