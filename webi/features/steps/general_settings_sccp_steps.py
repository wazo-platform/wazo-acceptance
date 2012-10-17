# -*- coding: utf-8 -*-

from lettuce import step, world
from xivo_lettuce import form
from xivo_lettuce.common import open_url
from xivo_lettuce.manager import asterisk_manager
from xivo_lettuce.manager_ws import sccp_general_settings_manager_ws as sccp_manager
from selenium.webdriver.support.select import Select


@step('Given the directmedia option is disabled')
def given_the_directmedia_option_is_disabled(step):
    sccp_manager.disable_directmedia()


@step('Given the directmedia option is enabled')
def given_the_directmedia_option_is_enabled(step):
    sccp_manager.enable_directmedia()


@step('Given the dial timeout is at (\d+) seconds')
def given_the_dial_timeout_is_at_x_seconds(step, timeout):
    sccp_manager.set_dialtimeout(timeout)


@step('Given the language option is at "([^"]*)"')
def given_the_language_option_is_at(step, language):
    sccp_manager.set_language(language)


@step('Given I am on the SCCP General Settings page')
def given_i_am_on_the_sccp_general_settings_page(step):
    open_url('sccpgeneralsettings')


@step('When I click the directmedia checkbox')
def when_i_click_the_directmedia_checkbox(step):
    directmedia_checkbox = world.browser.find_element_by_id("it-sccpgeneralsettings-directmedia")
    directmedia_checkbox.click()


@step('When I submit the form')
def when_i_submit_the_form(step):
    form.submit_form()


@step('When I change the dial timeout to "([^"]*)"')
def when_i_change_the_dial_timeout(step, timeout):
    dialtimeout_input = world.browser.find_element_by_id('it-sccpgeneralsettings-dialtimeout')
    dialtimeout_input.clear()
    dialtimeout_input.send_keys(timeout)


@step('When I select the language "([^"]*)"')
def when_i_select_the_language(step, language):
    language_dropdown = Select(world.browser.find_element_by_id('it-sccpgeneralsettings-language'))
    language_dropdown.select_by_visible_text(language)


@step('Then the option "([^"]*)" is at "([^"]*)" in sccp.conf')
def then_the_option_is_at_x_in_sccp_conf(step, option, expected_value):
    value = asterisk_manager.get_asterisk_conf("sccp.conf", option)
    assert(value == expected_value)

