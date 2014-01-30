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

from hamcrest import assert_that, equal_to, has_items
from lettuce import step
from xivo_lettuce import common
from xivo_lettuce import form
from xivo_acceptance.helpers import cti_helper


@step(u'Given I have a sheet model named "([^"]*)" with the variables:')
def given_i_have_a_sheet_model_named_group1_with_the_variables(step, call_form_name):
    variables = [l['variable'] for l in step.hashes]
    cti_helper.add_call_form_model(call_form_name, variables)


@step(u'^Given I assign the sheet "([^"]*)" to the "(.+)" event$')
def given_i_assign_model_to_event(step, call_form_name, event):
    cti_helper.set_call_form_model_on_event(call_form_name, event)


@step(u'Given I have a sheet model with custom UI:')
def given_i_have_a_sheet_model_with_custom_ui(step):
    sheet = step.hashes.pop()
    common.remove_element_if_exist('sheet', sheet['name'])
    common.open_url('sheet', 'add')

    form.input.set_text_field_with_label('Name :', sheet['name'])
    common.go_to_tab('Sheet')
    form.set_text_field_with_id('it-sheetactions-qtui', sheet['path to ui'])
    cti_helper.add_sheet_field(title='', type='form', default_value='', display_value='qtui')

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
    res = cti_helper.get_infos_in_custom_sheet()
    expected = step.hashes

    assert_that(res, has_items(*expected))
