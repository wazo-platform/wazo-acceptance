# -*- coding: utf-8 -*-

import time

from lettuce.decorators import step
from lettuce.registry import world
from selenium.common.exceptions import NoSuchElementException

from xivo_lettuce.common import *

OUTCALL_URL = '/service/ipbx/index.php/call_management/outcall/%s'

def _open_add_outcall_url():
    URL = OUTCALL_URL % '?act=add'
    world.browser.get('%s%s' % (world.url, URL))


def _open_list_outcall_url():
    URL = OUTCALL_URL % ('?act=list')
    world.browser.get('%s%s' % (world.url, URL))


def _exten_line(exten):
    """Find the line of an outcall exten in the list of an outcall extens."""
    return world.browser.find_element_by_xpath(
        "//table[@id='list_exten']//tr[.//input[@name='dialpattern[exten][]' and @value='%s']]" % exten)


@step(u'Given there is no outcall "([^"]*)"')
def given_there_is_no_outcall(step, name):
    _open_list_outcall_url()
    try:
        remove_line(name)
    except NoSuchElementException:
        pass


@step(u'When I create an outcall with name "([^"]*)" and trunk "([^"]*)"')
def when_i_create_an_outcall_with_name_and_trunk(step, name, trunk):
    _open_add_outcall_url()
    input_name = world.browser.find_element_by_id('it-outcall-name', 'Outcall form not loaded')
    input_name.send_keys(name)

    # Wait for the Javascript to fill the trunk list
    time.sleep(world.timeout)

    input_trunk = world.browser.find_element_by_xpath(
        "//div[@id='outcalltrunklist']//div[@class='available']//li[contains(@title, %s)]//a" % trunk)
    input_trunk.click()

    # Wait for the Javascript to move the trunk
    time.sleep(world.timeout)

    submit_form()


@step(u'Then there is an outcall "([^"]*)"')
def then_there_is_an_outcall(step, name):
    _open_list_outcall_url()
    assert find_line(name) is not None


@step(u'Given there is an outcall "([^"]*)" with trunk "([^"]*)"')
def given_there_is_an_outcall(step, name, trunk):
    _open_list_outcall_url()
    try:
        find_line(name)
    except NoSuchElementException:
        step.given(u'When I create an outcall with name "%s" and trunk "%s"' % (name, trunk))


@step(u'When I remove the outcall "([^"]*)"')
def when_i_remove_the_outcall(step, name):
    _open_list_outcall_url()
    remove_line(name)


@step(u'Then there is no outcall "([^"]*)"')
def then_there_is_no_outcall(step, name):
    _open_list_outcall_url()
    try:
        find_line(name)
    except NoSuchElementException:
        pass
    else:
        assert False


@step(u'I go to the outcall "([^"]*)", tab "([^"]*)"')
def i_go_to_the_outcall_tab(step, name, tab):
    _open_list_outcall_url()
    edit_line(name)
    go_to_tab(tab)


@step(u'Given I don\'t see any exten "([^"]*)"')
def given_i_dont_see_any_exten(step, exten):
    try:
        then_i_dont_see_any_exten(step, exten)
    except AssertionError:
        when_i_remove_the_exten(step, exten)
        submit_form()


@step(u'When I add an exten')
def when_i_add_an_exten(step):
    add_button = world.browser.find_element_by_id('lnk-add-row', 'Can\'t add an exten')
    add_button.click()


@step(u'When I set the exten to "([^"]*)"')
def when_i_set_the_exten_to(step, exten):
    input_exten = world.browser.find_elements_by_xpath(
        "//table[@id='list_exten']//input[@name='dialpattern[exten][]']")[-1]
    input_exten.send_keys(exten)


@step(u'Then I see an exten "([^"]*)"')
def then_i_see_an_exten(step, exten):
    exten_element = _exten_line(exten).find_element_by_xpath(
        ".//input[@name='dialpattern[exten][]']")
    assert exten_element is not None


@step(u'Given I see an exten "([^"]*)"')
def given_i_see_an_exten(step, exten):
    try:
        then_i_see_an_exten(step, exten)
    except NoSuchElementException:
        when_i_add_an_exten(step)
        when_i_set_the_exten_to(step, exten)
        submit_form()


@step(u'When I remove the exten "([^"]*)"')
def when_i_remove_the_exten(step, exten):
    delete_button = _exten_line(exten).find_element_by_id('lnk-del-row')
    delete_button.click()
    # Wait for the Javascript to remove the line
    time.sleep(world.timeout)


@step(u'Then I don\'t see any exten "([^"]*)"')
def then_i_dont_see_any_exten(step, exten):
    try:
        _exten_line(exten)
    except NoSuchElementException:
        pass
    else:
        assert False
