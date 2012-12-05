# -*- coding: utf-8 -*-

from lettuce import world
from xivo_ws import SIPTrunk


def add_trunksip(host, name, context='default', type='friend'):
    sip_trunk = SIPTrunk()
    sip_trunk.name = name
    sip_trunk.username = sip_trunk.name
    sip_trunk.secret = sip_trunk.name
    sip_trunk.context = context
    sip_trunk.host = host
    sip_trunk.type = type
    world.ws.sip_trunks.add(sip_trunk)


def add_or_replace_trunksip(host, name, context='default'):
    delete_trunksips_with_name(name)
    add_trunksip(host, name, context)


def delete_trunksips_with_name(name):
    sip_trunks = _search_trunksip_with_name(name)
    for sip_trunk in sip_trunks:
        world.ws.sip_trunks.delete(sip_trunk.id)


def find_trunksip_id_with_name(name):
    sip_trunk = _find_trunksip_with_name(name)
    return sip_trunk.id


def _find_trunksip_with_name(name):
    sip_trunks = _search_trunksip_with_name(name)
    if len(sip_trunks) != 1:
        raise Exception('expecting 1 sip trunk with name %r; found %s' %
                        (name, len(sip_trunks)))
    return sip_trunks[0]


def _search_trunksip_with_name(name):
    return world.ws.sip_trunks.search_by_name(name)
