# -*- coding: utf-8 -*-

# Copyright (C) 2013-2016 Avencall
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

from lettuce import step, world

import logging

logger = logging.getLogger(__name__)


@step(u'Given the user "([^"]*)" with the following func keys:')
def given_the_user_firstname_with_the_following_func_keys(step, username):
    firstname, lastname = username.split()
    user = world.confd_client.users.list(firstname=firstname, lastname=lastname)['items'][0]
    for line_number, line in enumerate(step.hashes, 1):
        funckey = _build_funckey(line)
        world.confd_client.users(user['uuid']).update_funckey(line_number, funckey)


def _build_funckey(line):
    type_ = line['destination_type']
    if type_ == 'forward':
        exten = line['destination_exten'] if line['destination_exten'] else None
        destination = {'type': type_,
                       'forward': line['destination_forward'],
                       'exten': exten}
    elif type_ == 'service':
        destination = {'type': type_,
                       'service': line['destination_service']}

    str_bool = {'true': True,
                'false': False}

    return {'blf': str_bool.get(line.get('blf')),
            'label': line.get('label'),
            'destination': destination}
