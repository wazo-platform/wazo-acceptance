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

from hamcrest import assert_that, equal_to, has_items
from lettuce import step, world
from selenium.webdriver.support.select import Select
from xivo_lettuce import common
from xivo_lettuce import form
from xivo_acceptance.helpers import cti_helper


EVENT_ELEMENT_MAP = {
    'Dial': 'it-dial',
    'Link': 'it-link',
    'Unlink': 'it-unlink',
    'Incoming DID': 'it-incomingdid',
    'Hangup': 'it-hangup',
}


@step(u'Given I have a sheet model named "([^"]*)" with the variables:')
def given_i_have_a_sheet_model_named_group1_with_the_variables(step, sheet_name):
    common.remove_element_if_exist('sheet', sheet_name)
    common.open_url('sheet', 'add')
    form.input.set_text_field_with_label('Name :', sheet_name)
    common.go_to_tab('Sheet')
    for line in step.hashes:
        _add_sheet_variable(line['variable'])
    form.submit.submit_form()


def _add_sheet_variable(variable_name):
    _add_sheet_field(title=variable_name, type='text', default_value='', display_value='{%s}' % variable_name)


def _add_sheet_field(title, type, default_value, display_value):
    add_button = world.browser.find_element_by_id('add_variable')
    add_button.click()
    new_variable_line = world.browser.find_element_by_xpath(
        "//tbody[@id='screens']/tr[last()]"
    )
    new_variable_name_input = new_variable_line.find_element_by_xpath(".//input[@name='screencol1[]']")
    new_variable_name_input.send_keys(title)

    new_variable_type_select = new_variable_line.find_element_by_xpath(".//select[@name='screencol2[]']")
    Select(new_variable_type_select).select_by_visible_text(type)

    new_variable_name_input = new_variable_line.find_element_by_xpath(".//input[@name='screencol3[]']")
    new_variable_name_input.send_keys(default_value)

    new_variable_value_input = new_variable_line.find_element_by_xpath(".//input[@name='screencol4[]']")
    new_variable_value_input.send_keys(display_value)


@step(u'^Given I assign the sheet "([^"]*)" to the "(.+)" event$')
def given_i_assign_the_sheet_group1_to_the_agent_linked_event(step, sheet_name, event_name):
    common.open_url('sheetevent')

    for name, element in EVENT_ELEMENT_MAP.iteritems():
        select_box = world.browser.find_element_by_id(element)

        if name == event_name:
            Select(select_box).select_by_visible_text(sheet_name)
        else:
            Select(select_box).select_by_index(0)

    form.submit.submit_form()


@step(u'Given I have a sheet model with custom UI:')
def given_i_have_a_sheet_model_with_custom_ui(step):
    sheet = step.hashes.pop()
    common.remove_element_if_exist('sheet', sheet['name'])
    common.open_url('sheet', 'add')

    form.input.set_text_field_with_label('Name :', sheet['name'])
    common.go_to_tab('Sheet')
    form.set_text_field_with_id('it-sheetactions-qtui', sheet['path to ui'])
    _add_sheet_field(title='', type='form', default_value='', display_value='qtui')

    form.submit.submit_form()


@step(u'Then I see a sheet with the following values:')
def then_i_see_a_sheet_with_the_following_values(step):
    res = cti_helper.get_sheet_infos()
    expected = step.hashes

    assert_that(res, has_items(*expected))


@step(u'Then I should not see any sheet')
def then_i_should_not_see_any_sheet(step):
    res = cti_helper.get_sheet_infos()
    assert_that(res, equal_to([]))


@step(u'Then I see a custom sheet with the following values:')
def then_i_see_a_custom_sheet_with_the_following_values(step):
    res = cti_helper.get_text_widget_infos()
    expected = step.hashes

    assert_that(res, has_items(*expected))
