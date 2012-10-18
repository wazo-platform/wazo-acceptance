# -*- coding: utf-8 -*-

from lettuce import world
from xivo_ws import IAXTrunk


def add_trunkiax(data):
    iaxtrunk = IAXTrunk()
    iaxtrunk.name = data['name']
    iaxtrunk.context = data['context']
    world.ws.iax_trunks.add(iaxtrunk)


def add_or_replace_trunkiax(data):
    delete_trunkiax_with_name(data['name'])
    add_trunkiax(data)


def delete_trunkiax_with_name(name):
    iax_trunks = _search_trunkiax_with_name(name)
    for iax_trunk in iax_trunks:
        world.ws.iax_trunks.delete(iax_trunk.id)


def _search_trunkiax_with_name(name):
    return world.ws.iax_trunks.search_by_name(name)
