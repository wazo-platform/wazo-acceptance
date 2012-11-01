# -*- coding: utf-8 -*-

import time

from lettuce import step
from selenium.webdriver.support.select import Select
from xivo_lettuce.common import webi_login, the_option_is_checked, remove_element_if_exist, \
    element_is_in_list, element_is_not_in_list, go_to_tab
from xivo_lettuce import form
from lettuce.registry import world
from xivo_lettuce.checkbox import Checkbox
from selenium.common.exceptions import NoSuchElementException
from xivo_lettuce.manager_ws.context_manager_ws import add_context


@step(u'When I login as (.*) with password (.*) in (.*)')
def when_i_login_the_webi(step, login, password, language):
    webi_login(login, password, language)


@step(u'Given there is a outcall context "([^"]*)"')
def given_there_is_a_ouctall_context(step, context_name):
    add_context(context_name, context_name, 'outcall')


@step(u'Given the option "([^"]*)" is (not )?checked')
def given_the_option_is_checked(step, option_name, checkstate):
    the_option_is_checked(option_name, checkstate, given=True)


@step(u'When I (un)?check the option "([^"]*)"')
def when_i_check_the_option_1(step, checkstate, option_label):
    option = world.browser.find_element_by_label(option_label)
    goal_checked = (checkstate is None)
    Checkbox(option).set_checked(goal_checked)


@step(u'When I (un)?check this option')
def when_i_check_this_option(step, checkstate):
    option = world.browser.find_element_by_label(world.last_option_label)
    goal_checked = (checkstate is None)
    Checkbox(option).set_checked(goal_checked)


@step(u'Given there is no ([a-z ]*) "([^"]*)"$')
def given_there_is_no_element(step, module, search):
    remove_element_if_exist(module, search)


@step(u'Then ([a-z ]*) "([^"]*)" is displayed in the list$')
def then_value_is_displayed_in_the_list(step, type, search):
    assert element_is_in_list(type, search)


@step(u'Then ([a-z ]*) "([^"]*)" is not displayed in the list$')
def then_value_is_not_displayed_in_the_list(step, type, search):
    assert element_is_not_in_list(type, search)


@step(u'I submit$')
def i_submit(step):
    time.sleep(1)
    form.submit_form()


@step(u'When I submit with errors')
def when_i_submit_with_errors(step):
    form.submit_form_with_errors()


@step(u'Then I see no errors')
def then_i_see_no_errors(step):
    # this step is there mostly for test readability; it's a no-op in most cases
    # since it's already checked when a form is submitted
    try:
        error_element = form.find_form_errors()
    except NoSuchElementException:
        pass
    else:
        raise form.FormErrorException(error_element.text)


@step(u'Then this option is (not )?checked')
def then_this_option_is_checked(step, checkstate):
    the_option_is_checked(world.last_option_label, checkstate)


@step(u'Then I see errors')
def then_i_see_errors(step):
    form.assert_form_errors()


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
