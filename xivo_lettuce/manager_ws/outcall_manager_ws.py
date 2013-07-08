# -*- coding: utf-8 -*-

# Copyright (C) 2013 Avencall
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

from lettuce import world
from xivo_ws import Outcall, OutcallExten


def list_outcalls():
    return world.ws.outcalls.list()


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


def add_or_replace_outcall(data):
    if _search_outcalls_with_name(data['name']):
        delete_outcalls_with_name(data['name'])
    add_outcall(data)


def delete_outcalls_with_name(name):
    for outcall in _search_outcalls_with_name(name):
        world.ws.outcalls.delete(outcall.id)


def delete_outcalls_with_context(context):
    for outcall in _find_all_outcalls_with_context(context):
        world.ws.outcalls.delete(outcall.id)


def _search_outcalls_with_name(name):
    name = unicode(name)
    outcalls = world.ws.outcalls.search(name)
    return [outcall for outcall in outcalls if outcall.name == name]


def _find_all_outcalls_with_context(context):
    outcalls = world.ws.outcalls.list()
    return [outcall for outcall in outcalls if outcall.context == context]
