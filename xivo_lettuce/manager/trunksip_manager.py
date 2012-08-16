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
    insert_id = world.ws.sip_trunk.add(sip_trunk)
    return insert_id


def del_trunksip(trunk_id):
    world.ws.sip_trunk.delete(trunk_id)
