# -*- coding: utf-8 -*-
from lettuce import step, world
from xivo_lettuce import common
from xivo_lettuce import form


@step(u'Given I have a sheet model named "([^"]*)" with the variables:')
def given_i_have_a_sheet_model_named_group1_with_the_variables(step, sheet_name):
    common.remove_element_if_exist('sheet', sheet_name)
    common.open_url('sheet', 'add')
    form.set_text_field('Name', sheet_name)
    common.go_to_tab('Sheet')
    for line in step.hashes:
        _add_sheet_variable(line['variable'])
    common.submit_form()


def _add_sheet_variable(variable_name):
    add_button = world.browser.find_element_by_id('add_variable')
    add_button.click()
    new_variable_line = world.browser.find_element_by_xpath(
        "//tbody[@id='screens']/tr[-1]"
    )
    new_variable_name_input = new_variable_line.find_element_by_xpath(".//input[@name='screencol1[]']")
    new_variable_name_input.send_keys(variable_name)
    new_variable_value_input = new_variable_line.find_element_by_xpath(".//input[@name='screencol4[]']")
    new_variable_value_input.send_keys('{%s}' % variable_name)


@step(u'^Given I assign the sheet "([^"]*)" to the agent linked event$')
def given_i_assign_the_sheet_group1_to_the_agent_linked_event(step, sheet_name):
    assert False, 'This step must be implemented'
