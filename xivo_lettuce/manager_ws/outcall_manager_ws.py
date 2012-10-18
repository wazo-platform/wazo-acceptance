# -*- coding: utf-8 -*-

from lettuce import world
from xivo_ws import Outcall, OutcallExten


def get_outcall_id_with_outcall_name(name):
    outcalls = world.ws.outcalls.list()
    for outcall in outcalls:
        if outcall.name == str(name):
            return outcall.id
    raise Exception('no outcall with outcall name %s' % name)


def delete_outcall_with_name_if_exists(name):
    try:
        outcall_id = get_outcall_id_with_outcall_name(name)
    except Exception:
        pass
    else:
        world.ws.outcalls.delete(outcall_id)


def add_outcall(data):
    outcall = Outcall()
    outcall.name = data['name']
    outcall.context = data['context']
    outcall.trunks = data['trunks']
    if 'extens' in data:
        extens = list()
        for exten in data['extens']:
            extension = exten['exten']
            stripnum = int(exten['stripnum'])
            caller_id = exten['caller_id']
            extens.append(OutcallExten(exten=extension, stripnum=stripnum, caller_id=caller_id))
        outcall.extens = extens
    world.ws.outcalls.add(outcall)
