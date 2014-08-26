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
from xivo_acceptance.action.restapi import line_extension_collection_action_restapi as action
from xivo_acceptance.helpers import extension_helper
from xivo_acceptance.helpers import line_sip_helper

FAKE_ID = 999999999


@step(u'Given extension "(\d+)@([\w-]+)" is associated to SIP line "([^"]*)"')
def given_extension_group1_is_associated_to_sip_line_group2(step, exten, context, sip_username):
    response = _associate_extension_to_line(exten, context, sip_username)
    assert_that(response.status, equal_to(201), str(response.data))


@step(u'When I get the list of extensions associated to a fake line')
def when_i_get_the_list_of_extensions_associated_to_a_fake_line(step):
    world.response = action.extensions_for_line(FAKE_ID)


@step(u'When I get the line associated to a fake extension')
def when_i_get_the_list_of_lines_associated_to_a_fake_extension(step):
    world.response = action.line_for_extension(FAKE_ID)


@step(u'When I get the line associated to extension "(\d+)@([\w-]+)"')
def when_i_get_the_line_associated_to_extension_group1(step, exten, context):
    extension = extension_helper.find_extension_by_exten_context(exten, context)
    world.response = action.line_for_extension(extension.id)


@step(u'When I get the list of extensions associated to SIP line "([^"]*)"')
def when_i_get_the_list_of_extensions_associated_to_sip_line_group1(step, sip_username):
    line_sip = line_sip_helper.get_by_username(sip_username)
    world.response = action.extensions_for_line(line_sip['id'])


@step(u'When I associate the extension "(\d+)@([\w-]+)" with a fake line')
def when_i_associate_the_extension_group1_with_a_fake_line(step, exten, context):
    extension = extension_helper.find_extension_by_exten_context(exten, context)
    world.response = action.associate_extension(FAKE_ID, extension.id)


@step(u'When I associate a fake extension to SIP line "([^"]*)"')
def when_i_associate_a_fake_extension_to_sip_line_group1(step, sip_username):
    line = line_sip_helper.get_by_username(sip_username)
    world.response = action.associate_extension(line['id'], FAKE_ID)


@step(u'When I associate extension "(\d+)@([\w-]+)" to SIP line "([^"]*)"')
def when_i_associate_extension_group1_to_sip_line_group2(step, exten, context, sip_username):
    world.response = _associate_extension_to_line(exten, context, sip_username)


@step(u'When I dissociate a fake extension from SIP line "([^"]*)"')
def when_i_dissociate_a_fake_extension_from_sip_line_group1(step, sip_username):
    line = line_sip_helper.get_by_username(sip_username)
    world.response = action.dissociate_extension(line['id'], FAKE_ID)


@step(u'When I dissociate extension "(\d+)@([\w-]+)" from SIP line "([^"]*)"')
def when_i_dissociate_extension_group1_from_sip_line_group2(step, exten, context, sip_username):
    extension = extension_helper.find_extension_by_exten_context(exten, context)
    line = line_sip_helper.get_by_username(sip_username)
    world.response = action.dissociate_extension(line['id'], extension.id)


def _associate_extension_to_line(exten, context, sip_username):
    extension = extension_helper.find_extension_by_exten_context(exten, context)
    line = line_sip_helper.get_by_username(sip_username)
    return action.associate_extension(line['id'], extension.id)
