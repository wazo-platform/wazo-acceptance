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

from lettuce import step, world
from hamcrest import assert_that, equal_to
from xivo_lettuce.xivoclient import xivoclient, xivoclient_step

CONFIG_URL = '/xivo/configuration/index.php'


@step(u'Given I go to the "([^"]*)" configuration page')
def given_i_go_to_the_1_configuration_page(step, section_name):
    world.browser.get('%s%s' % (world.host, CONFIG_URL))
    link = world.browser.find_element_by_link_text(section_name)
    link.click()


@step(u'Given I read the field "([^"]*)"')
def given_i_read_the_field_group1(step, field_label):
    input_field = world.browser.find_element_by_label(field_label)
    world.stocked_infos[field_label] = input_field.text


@step(u'Then the Xlet identity shows name as "([^"]*)" "([^"]*)"')
@xivoclient_step
def then_the_xlet_identity_shows_name_as_1_2(step, firstname, lastname):
    assert_that(world.xc_response, equal_to('passed'))


@step(u'Then the Xlet identity shows server name as field "([^"]*)"')
def then_the_xlet_identity_shows_server_name_as_field_1(step, field_label):
    @xivoclient
    def then_the_xlet_identity_shows_server_name_as_field_1_modified(field_value):
        pass
    field_value = world.stocked_infos[field_label]
    then_the_xlet_identity_shows_server_name_as_field_1_modified(field_value)
    assert_that(world.xc_response, equal_to('passed'))


@step(u'Then the Xlet identity shows phone number as "([^"]*)"')
@xivoclient_step
def then_the_xlet_identity_shows_phone_number_as_1(step, linenumber):
    assert_that(world.xc_response, equal_to('passed'))


@step(u'Then the Xlet identity shows a voicemail "([^"]*)"')
@xivoclient_step
def then_the_xlet_identity_shows_a_voicemail_1(step, vm_number):
    assert_that(world.xc_response, equal_to('passed'))


@step(u'Then the Xlet identity shows an agent "([^"]*)"')
@xivoclient_step
def then_the_xlet_identity_shows_an_agent_1(step, agent_number):
    assert_that(world.xc_response, equal_to('passed'))


@step(u'Then the Xlet identity does not show any agent')
@xivoclient_step
def then_the_xlet_identity_does_not_show_any_agent(step):
    assert_that(world.xc_response, equal_to('passed'))
