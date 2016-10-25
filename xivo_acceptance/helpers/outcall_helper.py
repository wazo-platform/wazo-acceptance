# -*- coding: utf-8 -*-

# Copyright (C) 2013-2014 Avencall
# Copyright (C) 2016 Proformatique Inc.
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


def add_or_replace_outcall(data):
    delete_outcalls_with_name(data['name'])
    add_outcall(data)


def add_outcall(data):
    outcall = world.confd_client.outcalls.create({'name': data['name']})
    for extension in data.get('extensions', []):
        world.confd_client.extensions.create({'exten': extension['exten'],
                                              'context': extension['context']})
        world.confd_client.outcalls(outcall['id']).add_extension(extension,
                                                                 strip_digits=int(extension['stripnum']),
                                                                 caller_id=extension['caller_id'])
    world.confd_client.outcalls(outcall['id']).update_trunks(data['trunks'])


def delete_outcalls_with_name(name):
    outcalls = world.confd_client.outcalls.list(name=name)['items']
    for outcall in outcalls:
        world.confd_client.outcalls.delete(outcall['id'])


def delete_outcalls_with_context(context):
    outcalls = world.confd_client.outcalls.list()
    for outcall in outcalls:
        for extension in outcall['extensions']:
            if extension['context'] == context:
                world.confd_client.outcalls(outcall['id']).delete()
                world.confd_client.extensions(extension['id']).delete()
