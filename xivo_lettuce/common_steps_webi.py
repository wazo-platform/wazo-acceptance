# -*- coding: utf-8 -*-

from lettuce.decorators import step
from selenium.webdriver.support.select import Select

from xivo_lettuce.common import *
from xivo_lettuce.manager import context_manager


@step(u'When I login as (.*) with password (.*) in (.*)')
def when_i_login_the_webi(step, login, password, language):
    webi_login(login, password, language)


@step(u'Given I am logged in')
def i_am_logged_in(step):
    if not logged():
        go_to_home_page()
        webi_login_as_default()


@step(u'Given the option "([^"]*)" is (not )?checked')
def given_the_option_is_checked(step, option_name, checkstate):
    the_option_is_checked(option_name, checkstate, given=True)


@step(u'Then the option "([^"]*)" is (not )?checked')
def then_the_option_is_checked(step, option_name, checkstate):
    the_option_is_checked(option_name, checkstate)


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


@step(u'Given there is no (?!queue)([a-z ]*) "([^"]*)"$')
def given_there_is_no_element(step, module, search):
    remove_element_if_exist(module, search)


@step(u'Then ([a-z ]*) "([^"]*)" is displayed in the list$')
def then_value_is_displayed_in_the_list(step, type, search):
    assert element_is_in_list(type, search) is True


@step(u'Then ([a-z ]*) "([^"]*)" is not displayed in the list$')
def then_value_is_not_displayed_in_the_list(step, type, search):
    assert element_is_not_in_list(type, search) is True


@step(u'I submit$')
def i_submit(step):
    time.sleep(1)
    submit_form()


@step(u'When I submit with errors')
def when_i_submit_with_errors(step):
    try:
        submit_form()
    except FormErrorException:
        pass
    else:
        raise Exception('No error occurred')


@step(u'Then I see no errors')
def then_i_see_no_errors(step):
    # this step is there mostly for test readability; it's a no-op in most cases
    # since it's already checked when a form is submitted
    try:
        error_element = find_form_errors()
    except NoSuchElementException:
        pass
    else:
        raise FormErrorException(error_element.text)


@step(u'Then this option is (not )?checked')
def then_this_option_is_checked(step, checkstate):
    the_option_is_checked(world.last_option_label, checkstate)


@step(u'Then I get errors')
def then_i_get_errors(step):
    assert_form_errors()


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


@step(u'I start the XiVO Client')
def i_start_the_xivo_client(step):
    run_xivoclient()

    # Waiting for the listening socket to open
    time.sleep(1)

    try:
        world.xc_socket.connect('/tmp/xivoclient')
    except:
        world.xc_process.terminate()
        raise


@step(u'I go to the XiVO Client configuration')
@xivoclient_step
def i_go_to_the_xivo_client_configuration(step):
    pass


@step(u'I close the XiVO Client configuration')
@xivoclient_step
def i_close_the_xivo_client_configuration(step):
    pass


@step(u'I log in the XiVO Client as "([^"]*)", pass "([^"]*)"')
def i_log_in_the_xivo_client_as_1_pass_2(step, login, password):
    i_log_in_the_xivo_client_to_host_1_as_2_pass_3(get_host_address(),
                                                   login,
                                                   password)
    assert world.xc_response == 'OK'


@step(u'I log in the XiVO Client as "([^"]*)", pass "([^"]*)", unlogged agent')
def i_log_in_the_xivo_client_as_1_pass_2_unlogged_agent(step, login, password):
    i_log_in_the_xivo_client_to_host_1_as_2_pass_3_unlogged_agent(get_host_address(),
                                                                  login,
                                                                  password)
    assert world.xc_response == 'OK'


@step(u'I can\'t log in the XiVO Client as "([^"]*)", pass "([^"]*)"')
def i_cant_log_in_the_xivo_client_as_1_pass_2(step, login, password):
    i_log_in_the_xivo_client_to_host_1_as_2_pass_3(get_host_address(),
                                                   login,
                                                   password)
    assert world.xc_response != 'OK'


@xivoclient
def i_log_in_the_xivo_client_to_host_1_as_2_pass_3(host, login, password):
    pass


@xivoclient
def i_log_in_the_xivo_client_to_host_1_as_2_pass_3_unlogged_agent(host, login, password):
    pass


@step(u'I log out of the XiVO Client')
@xivoclient_step
def i_log_out_of_the_xivo_client(step):
    assert world.xc_response == 'OK'


@step(u'I stop the XiVO Client')
def i_stop_the_xivo_client(step):
    i_stop_the_xivo_client()
