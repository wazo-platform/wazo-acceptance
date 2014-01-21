# -*- coding: utf-8 -*-

# Copyright (C) 2013-2014 Avencall
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

from hamcrest import assert_that, equal_to, has_key, has_entries, has_item
from lettuce import step, world

from xivo_acceptance.action.restapi import line_action_restapi
from xivo_acceptance.helpers import line_helper
from xivo_acceptance.helpers import line_sip_helper


@step(u'Given I have the following lines:')
def given_i_have_the_following_lines(step):
    for lineinfo in step.hashes:
        _delete_line(lineinfo)
        _create_line(lineinfo)


@step(u'Given I have no line with id "([^"]*)"')
def given_i_have_no_line_with_id_group1(step, line_id):
    line_id = int(line_id)
    line_helper.delete_line(line_id)


def _delete_line(lineinfo):
    if 'id' in lineinfo:
        line_helper.delete_line(int(lineinfo['id']))
    if 'username' in lineinfo:
        lines = line_helper.find_with_name(lineinfo['username'])
        for line in lines:
            line_helper.delete_line(line.id)


def _create_line(lineinfo):
    protocol = lineinfo['protocol'].lower()
    if protocol == 'sip':
        line_sip_helper.create_line_sip(lineinfo)
    else:
        line_helper.create(lineinfo)


@step(u'When I ask for the list of lines$')
def when_i_ask_for_the_list_of_lines(step):
    world.response = line_action_restapi.all_lines()


@step(u'When I ask for line with id "([^"]*)"')
def when_i_ask_for_line_with_id_group1(step, line_id):
    line_id = int(line_id)
    world.response = line_action_restapi.get(line_id)


@step(u'Then the line "([^"]*)" no longer exists')
def then_the_line_group1_no_longer_exists(step, line_id):
    response = line_action_restapi.get(line_id)
    assert_that(response.status, equal_to(404))


@step(u'Then I get a list containing the following lines:')
def then_i_get_a_list_containing_the_following_lines(step):
    line_response = world.response.data
    expected_lines = step.hashes

    assert_that(line_response, has_key('items'))
    lines = line_response['items']

    for expected_line in expected_lines:
        expected_line = _convert_line_parameters(expected_line)
        assert_that(lines, has_item(has_entries(expected_line)))


def _convert_line_parameters(line):

    if 'id' in line:
        line['id'] = int(line['id'])

    if 'device_slot' in line:
        line['device_slot'] = int(line['device_slot'])

    return line


@step(u'Then I get a line with the following parameters:')
def then_i_get_a_line_with_the_following_parameters(step):
    expected_line = _convert_line_parameters(step.hashes[0])
    line_response = world.response.data

    assert_that(line_response, has_entries(expected_line))
