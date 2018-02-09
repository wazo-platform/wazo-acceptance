# -*- coding: utf-8 -*-
# Copyright (C) 2013-2016 Avencall
# SPDX-License-Identifier: GPL-3.0+

from hamcrest import assert_that, has_items, equal_to
from lettuce import step
from xivo_acceptance.helpers import cti_helper
from xivo_acceptance.lettuce import common, form


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
    cti_helper.add_sheet_field(title='', display_type='form', default_value='', display_value='qtui')

    form.submit.submit_form()


@step(u'(?:Then|Given) I see a sheet with the following values:')
def then_i_see_a_sheet_with_the_following_values(step):
    res = common.wait_until(cti_helper.get_sheet_infos, tries=10)
    expected = step.hashes

    assert_that(res, has_items(*expected))


@step(u'Then I should not see any sheet')
def then_i_should_not_see_any_sheet(step):
    def assert_no_sheet():
        res = cti_helper.get_sheet_infos()
        assert_that(res, equal_to([]))
    common.wait_until_assert(assert_no_sheet, tries=10)


@step(u'Then I see a custom sheet with the following values:')
def then_i_see_a_custom_sheet_with_the_following_values(step):
    res = cti_helper.get_infos_in_custom_sheet()
    expected = step.hashes

    assert_that(res, has_items(*expected))


@step(u'When I fill a custom sheet with the following values:')
def when_i_fill_a_custom_sheet_with_the_following_values(step):
    cti_helper.set_infos_in_custom_sheet(step.hashes)


@step(u'When I close all sheets')
def when_i_close_all_sheets(step):
    cti_helper.close_all_sheets()
