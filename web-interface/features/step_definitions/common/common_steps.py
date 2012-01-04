# -*- coding: utf-8 -*-

import time

from lettuce.decorators import step
from lettuce.registry import world
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException
from selenium.webdriver.support.select import Select

from common.common import *
from checkbox import Checkbox

@step(u'Given the option "([^"]*)" is (not )?checked')
def given_the_option_is_checked(step, option_name, checkstate):
    the_option_is_checked(option_name, checkstate, given = True)

@step(u'Then the option "([^"]*)" is (not )?checked')
def then_the_option_is_checked(step, option_name, checkstate):
    the_option_is_checked(option_name, checkstate)

@step(u'When I (un)?check this option')
def when_i_check_this_option(step, checkstate):
    option = world.browser.find_element_by_label(world.last_option_label)
    goal_checked = (checkstate is None)
    Checkbox(option).set_checked(goal_checked)

@step(u'When I submit$')
def when_i_submit(step):
    submit_form()

@step(u'When I submit with errors')
def when_i_submit_with_errors(step):
    try:
        submit_form()
    except FormErrorException:
        pass

@step(u'Then this option is (not )?checked')
def then_this_option_is_checked(step, checkstate):
    the_option_is_checked(world.last_option_label, checkstate)

@step(u'Then I get errors')
def then_i_get_errors(step):
    assert find_form_errors() is not None

@step(u'I set the select field "([^"]*)" to "([^"]*)"')
def when_i_set_the_select_field_1_to_2(step, label, value):
    select_input = world.browser.find_element_by_label(label)
    Select(select_input).select_by_visible_text(value)

@step(u'the select field "([^"]*)" is set to "([^"]*)"')
def the_select_field_1_is_set_to_2(step, label, value):
    select_input = world.browser.find_element_by_label(label)
    selected = Select(select_input).first_selected_option
    assert selected.text == value

@step(u'I set the text field "([^"]*)" to "([^"]*)"')
def i_set_the_text_field_1_to_2(step, label, value):
    text_input = world.browser.find_element_by_label(label)
    text_input.clear()
    text_input.send_keys(value)

@step(u'the text field "([^"]*)" is set to "([^"]*)"')
def the_text_field_1_is_set_to_2(step, label, value):
    text_input = world.browser.find_element_by_label(label)
    assert text_input.get_attribute('value') == value

@step('I go to the "([^"]*)" tab')
def i_go_to_the_1_tab(step, tab_text):
    go_to_tab(tab_text)
