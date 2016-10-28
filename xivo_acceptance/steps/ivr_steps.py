# -*- coding: utf-8 -*-

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

from xivo_acceptance.helpers.ivr_helper import add_or_replace_ivr
from xivo_acceptance.helpers.user_helper import get_by_firstname_lastname


@step(u'Given there are IVR with infos:')
def given_there_are_incalls_with_infos(step):
    for ivr in step.hashes:
        add_or_replace_ivr(ivr)


@step(u'Given the IVR "([^"]*)" choices are:')
def given_the_ivr_group1_choices_are(step, ivr_name):
    choices = []
    for data in step.hashes:
        if data['destination_type'] == 'user':
            firstname, lastname = data['destination_arg'].split(' ', 1)
            user = get_by_firstname_lastname(firstname, lastname)
            destination = {
                'type': 'user',
                'user_id': user['id'],
            }
        elif data['destination_type'] == 'none':
            destination = {'type': 'none'}
        else:
            raise AssertionError('unknown destination type {}'.format(data['destination_type']))
        choices.append({'exten': data['exten'], 'destination': destination})
    _update_ivr(ivr_name, {'choices': choices})


def _update_ivr(ivr_name, body):
    ivr = world.confd_client.ivr.list(name=ivr_name)['items'][0]
    body['id'] = ivr['id']
    world.confd_client.ivr.update(body)
