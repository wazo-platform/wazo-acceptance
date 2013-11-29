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

from hamcrest import assert_that, equal_to
from lettuce import step, world

from xivo_acceptance.action.restapi import line_action_restapi
from xivo_acceptance.action.restapi import line_extension_action_restapi as line_extension_action
from xivo_acceptance.helpers import line_helper
from xivo_acceptance.helpers import line_sip_helper
from xivo_acceptance.helpers import extension_helper


@step(u'Given I only have the following lines:')
def given_i_created_the_following_lines(step):
    line_helper.delete_all()
    for lineinfo in step.hashes:
        _create_line(lineinfo)


@step(u'Given I have the following lines:')
def given_i_have_the_following_lines(step):
    for lineinfo in step.hashes:
        _delete_line(lineinfo)
        _create_line(lineinfo)


def _delete_line(lineinfo):
    if 'id' in lineinfo:
        line_helper.delete_line(int(lineinfo['id']))


def _create_line(lineinfo):
    protocol = lineinfo['protocol'].lower()
    if protocol == 'sip':
        line_sip_helper.create_line_sip(lineinfo)
    else:
        line_helper.create(lineinfo)


@step(u'Given I have no lines')
def given_there_are_no_lines(step):
    line_helper.delete_all()


@step(u'When I ask for the list of lines$')
def when_i_ask_for_the_list_of_lines(step):
    world.response = line_action_restapi.all_lines()


@step(u'When I ask for the list of user_links with line_id "([^"]*)"$')
def when_i_ask_for_the_list_of_user_links_with_line_id(step, line_id):
    world.response = line_action_restapi.all_user_links_by_line_id(line_id)


@step(u'Then the line "([^"]*)" no longer exists')
def then_the_line_group1_no_longer_exists(step, line_id):
    response = line_action_restapi.get(line_id)
    assert_that(response.status, equal_to(404))


@step(u'Given I have no line with id "([^"]*)"')
def given_i_have_no_line_with_id_group1(step, line_id):
    line_id = int(line_id)
    line_helper.delete_line(line_id)


@step(u'When I link extension "([^"]*)" with line id "([^"]*)"')
def when_i_link_extension_group1_with_line_id_group2(step, extension, line_id):
    exten, context = extension.split('@')
    extension = extension_helper.find_extension_by_exten_context(exten, context)
    world.response = line_extension_action.associate(line_id, extension.id)
    print "RESPONSE"
    print world.response.data


@step(u'When I link extension id "([^"]*)" with line id "([^"]*)"')
def when_i_link_extension_id_group1_with_line_id_group2(step, extension_id, line_id):
    world.response = line_extension_action.associate(line_id, extension_id)
