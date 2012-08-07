# -*- coding: utf-8 -*-

from lettuce import step, world

from selenium.common.exceptions import NoSuchElementException
from xivo_lettuce.checkbox import Checkbox
from xivo_lettuce.common import go_to_tab, open_url, submit_form
from xivo_lettuce.manager.iax_general_manager import find_call_limit_line,\
    find_call_limit_lines


@step(u'I go on the General Settings > IAX Protocol page, tab "([^"]*)"')
def i_go_on_the_general_settings_iax_protocol_page_tab(step, tab):
    open_url('general_iax')
    go_to_tab(tab)


@step(u'Given I don\'t see any call limit to "([^"]*)" netmask "([^"]*)"')
def given_i_don_t_see_any_call_limit_to_netmask_(step, destination, netmask):
    try:
        lines = find_call_limit_lines(destination, netmask)
    except NoSuchElementException:
        return
    when_i_remove_the_call_limits_to_netmask(step, destination, netmask)
    submit_form()


@step(u'When I add a call limit')
def when_i_add_a_call_limit(step):
    add_button = world.browser.find_element_by_xpath("//a[@title='Add a call limit']")
    add_button.click()
    world.new_line = world.browser.find_elements_by_xpath("//tbody[@id='disp']//tr")[-1]


@step(u'When I set the destination to "([^"]*)"')
def when_i_set_the_destination_to(step, destination):
    input_destination = world.new_line.find_element_by_name('calllimits[destination][]')
    input_destination.send_keys(destination)


@step(u'When I set the netmask to "([^"]*)"')
def when_i_set_the_netmask_to(step, netmask):
    input_netmask = world.new_line.find_element_by_name('calllimits[netmask][]')
    input_netmask.send_keys(netmask)


@step(u'When I set the call limit to "([^"]*)"')
def when_i_set_the_call_limit_to(step, limit):
    input_limit = world.new_line.find_element_by_name('calllimits[calllimits][]')
    input_limit.send_keys(limit)


@step(u'Then I see a call limit to "([^"]*)" netmask "([^"]*)" of "([^"]*)" calls')
def then_i_see_a_call_limit_to_netmask_of_calls(step, destination, netmask, limit):
    find_call_limit_line(destination, netmask, limit)


@step(u'Given I see a call limit to "([^"]*)" netmask "([^"]*)" of "([^"]*)" calls')
def given_i_see_a_call_limit_to_netmask_of_calls(step, destination, netmask, limit):
    try:
        find_call_limit_line(destination, netmask, limit)
    except NoSuchElementException:
        when_i_add_a_call_limit(step)
        when_i_set_the_destination_to(step, destination)
        when_i_set_the_netmask_to(step, netmask)
        when_i_set_the_call_limit_to(step, limit)
        submit_form()


@step(u'When I remove the call limits to "([^"]*)" netmask "([^"]*)"')
def when_i_remove_the_call_limits_to_netmask(step, destination, netmask):
    lines = find_call_limit_lines(destination, netmask)
    for line in lines:
        delete_button = line.find_element_by_xpath(".//a[@title='Delete this limit']")
        delete_button.click()
    submit_form()


@step(u'Then I don\'t see a call limit to "([^"]*)" netmask "([^"]*)"')
def then_i_don_t_see_a_call_limit_to_group1_netmask_group2(step, destination, netmask):
    try:
        find_call_limit_line(destination, netmask)
        assert False, 'the call limit has not been removed'
    except NoSuchElementException:
        pass


@step(u'Given the SRV lookup option is disabled')
def given_the_srv_lookup_option_is_disabled(step):
    option = _get_srv_lookup_option()

    if option.is_checked():
        option.uncheck()
        submit_form()

        option = _get_srv_lookup_option()
        assert not option.is_checked()


@step(u'When I enable the SRV lookup option')
def when_i_enable_the_srv_lookup_option(step):
    option = _get_srv_lookup_option()
    option.check()
    submit_form()


@step(u'Then the SRV lookup option is enabled')
def then_the_srv_lookup_option_is_enabled(step):
    option = _get_srv_lookup_option()
    assert option.is_checked()


def _get_srv_lookup_option():
    open_url('general_iax')
    go_to_tab('Default')
    option = Checkbox.from_label('SRV lookup')

    return option
