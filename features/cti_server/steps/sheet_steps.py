# -*- coding: utf-8 -*-

from lettuce import step, world
from xivo_lettuce import common
from xivo_lettuce import form
from selenium.webdriver.support.select import Select


EVENT_ELEMENT_MAP = {
    'Dial': 'it-dial',
    'Link': 'it-link',
    'Unlink': 'it-unlink',
    'Agent linked': 'it-agentlinked',
    'Agent unlinked': 'it-agentunlinked',
    'Incoming DID': 'it-incomingdid',
    'Hangup': 'it-hangup',
}


@step(u'Given I have a sheet model named "([^"]*)" with the variables:')
def given_i_have_a_sheet_model_named_group1_with_the_variables(step, sheet_name):
    common.remove_element_if_exist('sheet', sheet_name)
    common.open_url('sheet', 'add')
    form.set_text_field('Name :', sheet_name)
    common.go_to_tab('Sheet')
    for line in step.hashes:
        _add_sheet_variable(line['variable'])
    form.submit_form()


def _add_sheet_variable(variable_name):
    add_button = world.browser.find_element_by_id('add_variable')
    add_button.click()
    new_variable_line = world.browser.find_element_by_xpath(
        "//tbody[@id='screens']/tr[last()]"
    )
    new_variable_name_input = new_variable_line.find_element_by_xpath(".//input[@name='screencol1[]']")
    new_variable_name_input.send_keys(variable_name)

    new_variable_type_select = new_variable_line.find_element_by_xpath(".//select[@name='screencol2[]']")
    Select(new_variable_type_select).select_by_visible_text("text")

    new_variable_value_input = new_variable_line.find_element_by_xpath(".//input[@name='screencol4[]']")
    new_variable_value_input.send_keys('{%s}' % variable_name)


@step(u'^Given I assign the sheet "([^"]*)" to the "(.+)" event$')
def given_i_assign_the_sheet_group1_to_the_agent_linked_event(step, sheet_name, event_name):
    if event_name not in EVENT_ELEMENT_MAP:
        return
    common.open_url('sheetevent')
    element_id = EVENT_ELEMENT_MAP[event_name]
    select_box = world.browser.find_element_by_id(element_id)
    Select(select_box).select_by_visible_text(sheet_name)
    form.submit_form()
