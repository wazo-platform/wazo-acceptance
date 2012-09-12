# -*- coding: utf-8 -*-

from xivo_ws.objects.siptrunk import SIPTrunk
from lettuce.registry import world


def add_trunksip(host, name, context='default'):
    sip_trunk = SIPTrunk()
    sip_trunk.name = name
    sip_trunk.username = sip_trunk.name
    sip_trunk.secret = sip_trunk.name
    sip_trunk.context = context
    sip_trunk.host = host
    sip_trunk.type = 'friend'
    world.ws.sip_trunk.add(sip_trunk)


def add_or_replace_trunksip(host, name, context='default'):
    trunksips = find_trunksip_with_name(name)
    if len(trunksips) == 1:
        trunksip = trunksips[0]
        delete_trunksip_with_id(trunksip.id)
    add_trunksip(host, name, context)


def get_trunk_id_with_name(name):
    sip_trunks = find_trunksip_with_name(name)
    for sip_trunk in sip_trunks:
        if sip_trunk.name == str(name):
            return sip_trunk.id
    raise Exception('no sip_trunk with name "%s"', name)


def find_trunksip_with_name(name):
    return world.ws.sip_trunk.search(name)


def delete_trunksip_with_id(trunk_id):
    world.ws.sip_trunk.delete(trunk_id)
