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

from hamcrest import *
from lettuce import step, world

from xivo_acceptance.action.restapi import user_line_action_restapi
from xivo_acceptance.helpers import user_helper


@step(u'Given I have no user_line with the following parameters:')
def given_i_have_no_user_line_with_the_following_parameters(step):
    for data in step.hashes:
        user_line = _extract_parameters(data)
        world.response = user_line_action_restapi.delete_user_line(user_line['user_id'], user_line['line_id'])


@step(u'Given line "([^"]*)" is linked with user "([^"]*)" "([^"]*)"')
def given_line_group1_is_linked_with_user_group2_group3(step, line_id, firstname, lastname):
    line_id = int(line_id)
    user_id = user_helper.find_user_id_with_firstname_lastname(firstname, lastname)
    world.response = user_line_action_restapi.create_user_line(user_id, {'line_id': line_id})


@step(u'When I create an empty user_line')
def when_i_create_an_empty_user_line(step):
    world.response = user_line_action_restapi.create_user_line(1, {})


@step(u'When I create the following user_line via RESTAPI:')
def when_i_create_the_following_user_lines(step):
    for data in step.hashes:
        user_line = _extract_parameters(data)
        world.response = user_line_action_restapi.create_user_line(user_line['user_id'], user_line)


@step(u'When I request the lines associated to user id "([^"]*)" via RESTAPI')
def when_i_request_the_lines_associated_to_user_id_group1_via_restapi(step, user_id):
    world.response = user_line_action_restapi.get_user_line(user_id)


@step(u'When I dissociate the following user_line via RESTAPI:')
def when_i_dossociate_the_following_user_lines(step):
    for data in step.hashes:
        user_line = _extract_parameters(data)
        world.response = user_line_action_restapi.delete_user_line(user_line['user_id'], user_line['line_id'])


def _extract_parameters(user_line):
    if 'user_id' in user_line and user_line['user_id'].isnumeric():
        user_line['user_id'] = int(user_line['user_id'])

    if 'line_id' in user_line and user_line['line_id'].isnumeric():
        user_line['line_id'] = int(user_line['line_id'])

    if 'main_line' in user_line and user_line['main_line'] in ['True', 'False']:
        user_line['main_line'] = user_line['main_line'] == 'True'

    if 'main_user' in user_line and user_line['main_user'] in ['True', 'False']:
        user_line['main_user'] = user_line['main_user'] == 'True'

    return user_line
