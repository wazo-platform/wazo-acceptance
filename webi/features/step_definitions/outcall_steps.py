# -*- coding: utf-8 -*-

import time

from lettuce.decorators import step
from lettuce.registry import world
from selenium.common.exceptions import NoSuchElementException
from xivo_lettuce.common import edit_line, find_line, go_to_tab, open_url, \
    remove_line, submit_form
from xivo_lettuce.manager.outcall_manager import exten_line
from xivo_lettuce.manager_ws import trunksip_manager_ws, outcall_manager_ws


@step(u'Given there is an outcall "([^"]*)" with trunk "([^"]*)"')
def given_there_is_an_outcall(step, outcall_name, trunk_name):
    trunksip_manager_ws.add_or_replace_trunksip('host', trunk_name)
    trunk_id = trunksip_manager_ws.get_trunk_id_with_name(trunk_name)
    data = {'name': outcall_name,
            'context': 'to-extern',
            'trunks': [trunk_id]}
    outcall_manager_ws.add_outcall(data)


@step(u'Given I don\'t see any exten "([^"]*)"')
def given_i_dont_see_any_exten(step, exten):
    try:
        then_i_dont_see_any_exten(step, exten)
    except AssertionError:
        when_i_remove_the_exten(step, exten)
        submit_form()


@step(u'Given I see an exten "([^"]*)"')
def given_i_see_an_exten(step, exten):
    try:
        then_i_see_an_exten(step, exten)
    except NoSuchElementException:
        when_i_add_an_exten(step)
        when_i_set_the_exten_to(step, exten)
        submit_form()


@step(u'Given there is no outcall "([^"]*)"')
def given_there_is_no_outcall(step, name):
    outcall_manager_ws.delete_outcall_with_name_if_exists(name)


@step(u'When I create an outcall with name "([^"]*)" and trunk "([^"]*)"')
def when_i_create_an_outcall_with_name_and_trunk(step, name, trunk):
    open_url('outcall', 'add')
    input_name = world.browser.find_element_by_id('it-outcall-name', 'Outcall form not loaded')
    input_name.send_keys(name)

    # Wait for the Javascript to fill the trunk list
    time.sleep(1)

    input_trunk = world.browser.find_element_by_xpath(
        "//div[@id='outcalltrunklist']//div[@class='available']//li[contains(@title, %s)]//a" % trunk)
    input_trunk.click()

    # Wait for the Javascript to move the trunk
    time.sleep(1)

    submit_form()


@step(u'When I remove the outcall "([^"]*)"')
def when_i_remove_the_outcall(step, name):
    open_url('outcall', 'list')
    remove_line(name)


@step(u'I go to the outcall "([^"]*)", tab "([^"]*)"')
def i_go_to_the_outcall_tab(step, name, tab):
    open_url('outcall', 'list')
    edit_line(name)
    go_to_tab(tab)


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
    exten_element = exten_line(exten).find_element_by_xpath(
        ".//input[@name='dialpattern[exten][]']")
    assert exten_element is not None


@step(u'When I remove the exten "([^"]*)"')
def when_i_remove_the_exten(step, exten):
    delete_button = exten_line(exten).find_element_by_id('lnk-del-row')
    delete_button.click()
    # Wait for the Javascript to remove the line
    time.sleep(1)


@step(u'Then I don\'t see any exten "([^"]*)"')
def then_i_dont_see_any_exten(step, exten):
    try:
        exten_line(exten)
    except NoSuchElementException:
        pass
    else:
        assert False


@step(u'Then there is no outcall "([^"]*)"')
def then_there_is_no_outcall(step, name):
    open_url('outcall', 'list')
    try:
        find_line(name)
    except NoSuchElementException:
        pass
    else:
        assert False
