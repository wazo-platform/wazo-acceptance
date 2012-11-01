# -*- coding: utf-8 -*-

from lettuce import world
from xivo_ws import Outcall, OutcallExten


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


def delete_outcalls_with_name(name):
    for outcall in _search_outcalls_with_name(name):
        world.ws.outcalls.delete(outcall.id)


def _search_outcalls_with_name(name):
    name = unicode(name)
    outcalls = world.ws.outcalls.search(name)
    return [outcall for outcall in outcalls if outcall.name == name]
