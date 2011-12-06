# -*- coding: utf-8 -*-

from lettuce.decorators import step
from lettuce.registry import world

from common.common import *

def _xpath_call_limit_line(destination=None, netmask=None, limit=None):
    xpath = "//tbody[@id='disp']/tr"
    filters = []
    if destination is not None:
        filters.append("td/input[@name='calllimits[destination][]' "
                                 "and @value='%s']" % destination)
    if netmask is not None:
        filters.append("td/input[@name='calllimits[netmask][]' "
                                 "and @value='%s']" % netmask)
    if limit is not None:
        filters.append("td/input[@name='calllimits[calllimits][]' "
                                 "and @value='%s']" % limit)
    if len(filters) > 0:
        xpath += "[" + ' and '.join(filters) + "]"
    return xpath

def _find_call_limit_line(destination=None, netmask=None, limit=None):
    xpath = _xpath_call_limit_line(destination, netmask, limit)
    line = world.browser.find_element_by_xpath(xpath)
    return line

def _find_call_limit_lines(destination=None, netmask=None, limit=None):
    xpath = _xpath_call_limit_line(destination, netmask, limit)
    lines = world.browser.find_elements_by_xpath(xpath)
    return lines

@step(u'I go on the General Settings > IAX Protocol page, tab "([^"]*)"')
def i_go_on_the_general_settings_iax_protocol_page_tab(step, tab):
    world.browser.get(world.url + 'service/ipbx/index.php/general_settings/iax/')
    go_to_tab(tab)

@step(u'Given I don\'t see any call limit to "([^"]*)" netmask "([^"]*)"')
def given_i_don_t_see_any_call_limit_to_netmask_(step, destination, netmask):
    try:
        lines = _find_call_limit_lines(destination, netmask)
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
    _find_call_limit_line(destination, netmask, limit)

@step(u'Given I see a call limit to "([^"]*)" netmask "([^"]*)" of "([^"]*)" calls')
def given_i_see_a_call_limit_to_netmask_of_calls(step, destination, netmask, limit):
    try:
        _find_call_limit_line(destination, netmask, limit)
    except NoSuchElementException:
        when_i_add_a_call_limit(step)
        when_i_set_the_destination_to(step, destination)
        when_i_set_the_netmask_to(step, netmask)
        when_i_set_the_call_limit_to(step, limit)
        submit_form()

@step(u'When I remove the call limits to "([^"]*)" netmask "([^"]*)"')
def when_i_remove_the_call_limits_to_netmask(step, destination, netmask):
    lines = _find_call_limit_lines(destination, netmask)
    for line in lines:
        delete_button = line.find_element_by_xpath(".//a[@title='Delete this limit']")
        delete_button.click()
    submit_form()

@step(u'Then I don\'t see a call limit to "([^"]*)" netmask "([^"]*)"')
def then_i_don_t_see_a_call_limit_to_group1_netmask_group2(step, destination, netmask):
    try:
        _find_call_limit_line(destination, netmask)
        assert False, 'the call limit has not been removed'
    except NoSuchElementException:
        pass
