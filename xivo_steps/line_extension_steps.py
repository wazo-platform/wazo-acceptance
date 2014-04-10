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

from hamcrest import assert_that, equal_to

from lettuce import step, world
from xivo_acceptance.action.restapi import line_extension_action_restapi as line_extension_action
from xivo_acceptance.helpers import extension_helper


@step(u'Given line "([^"]*)" is linked with extension "([^"]*)"')
def given_line_group1_is_linked_with_extension_group2(step, line_id, extension):
    _link_line_and_extension(line_id, extension)
    assert_that(world.response.status, equal_to(201), unicode(world.response.data))


@step(u'When I send a request for the line associated to a fake extension')
def when_i_send_a_request_for_the_line_associated_to_a_fake_extension(step):
    world.response = line_extension_action.get_from_extension(999999999)


@step(u'When I send a request for the line associated to extension with exten "(\d+)@([\w-]+)"')
def when_i_send_a_request_for_the_line_associated_to_extension_with_exten_group1(step, exten, context):
    extension = extension_helper.get_by_exten_context(exten, context)
    world.response = line_extension_action.get_from_extension(extension.id)


@step(u'When I link extension "([^"]*)" with line id "([^"]*)"')
def when_i_link_extension_group1_with_line_id_group2(step, extension, line_id):
    _link_line_and_extension(line_id, extension)


def _link_line_and_extension(line_id, extension):
    exten, context = extension.split('@')
    extension = extension_helper.find_extension_by_exten_context(exten, context)
    world.response = line_extension_action.associate(line_id, extension.id)


@step(u'When I link extension id "([^"]*)" with line id "([^"]*)"')
def when_i_link_extension_id_group1_with_line_id_group2(step, extension_id, line_id):
    world.response = line_extension_action.associate(line_id, extension_id)


@step(u'When I send a request for the extension associated to line id "([^"]*)"')
def when_i_send_a_request_for_the_extension_associated_to_line_id_group1(step, line_id):
    world.response = line_extension_action.get(line_id)


@step(u'When I dissociate the extension associated to line id "([^"]*)"')
def when_i_dissociate_the_extension_associated_to_line_id_group1(step, line_id):
    world.response = line_extension_action.dissociate(line_id)
