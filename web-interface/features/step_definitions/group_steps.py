# -*- coding: utf-8 -*-

from lettuce.decorators import step
from lettuce.registry import world
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotVisibleException

GROUP_URL = '/service/ipbx/index.php/pbx_settings/groups/%s'


def _open_add_group_url():
    URL = GROUP_URL % '?act=add'
    world.browser.get('%s%s' % (world.url, URL))
    world.wait_for_id('it-groupfeatures-name', 'Group form not loaded')

def _open_list_group_url():
    URL = GROUP_URL % ('?act=list')
    world.browser.get('%s%s' % (world.url, URL))
    world.wait_for_name('fm-group-list', 'Group list not loaded')

def _type_group_name(group_name):
    world.wait_for_id('it-groupfeatures-name', 'Group form not loaded')
    world.group_name = group_name
    input_name = world.browser.find_element_by_id('it-groupfeatures-name')
    input_name.send_keys(group_name)

def _type_group_number(group_number):
    world.wait_for_id('it-groupfeatures-number', 'Group form not loaded')
    world.group_number = group_number
    input_number = world.browser.find_element_by_id('it-groupfeatures-number')
    input_number.send_keys(group_number)

def _type_context(context):
    select_context = world.browser.find_element_by_xpath('//select[@id="it-groupfeatures-context"]//option[@value="%s"]' % context)
    select_context.click()

def _submit_group_form():
    world.browser.find_element_by_id('it-submit').click()

def _remove_group_with_number(group_number):
    _open_list_group_url()
    try:
        delete_button = world.browser.find_element_by_xpath("//table[@id='table-main-listing']//tr[contains(.,'%s')]//a[@title='Delete']" % group_number)
        delete_button.click()
        alert = world.browser.switch_to_alert();
        alert.accept()
    except NoSuchElementException, ElementNotVisibleException:
        pass

def _remove_group_with_name(group_name):
    _open_list_group_url()
    try:
        delete_button = world.browser.find_element_by_xpath("//table[@id='table-main-listing']//tr[contains(.,'%s')]//a[@title='Delete']" % group_name)
        delete_button.click()
        alert = world.browser.switch_to_alert();
        alert.accept()
    except NoSuchElementException, ElementNotVisibleException:
        pass

def _group_is_saved(group_name):
    _open_list_group_url()
    try:
        group = world.browser.find_element_by_xpath("//table[@id='table-main-listing']//tr[contains(.,'%s')]" % (group_name))
        return group is not None
    except NoSuchElementException:
        return False

def _delete_all_group():
    from webservices.group import WsGroup
    wsg = WsGroup()
    wsg.clear()

@step(u'Given there is no group with number ([0-9]+)')
def given_there_is_no_group_with_number(step, number):
    _remove_group_with_number(number)

@step(u'Given there is no group with name ([\w]+)')
def given_there_is_no_group_with_name(step, name):
    _remove_group_with_name(name)

@step(u'When I create a group (.*) with number ([0-9]+)')
def when_i_create_group_with_number(step, group_name, group_number):
    import context_steps as ctx
    ctx.when_i_edit_a_context(step, 'default')
    ctx.when_i_edit_group_ranges(step)
    ctx.when_i_add_group_interval(step, 5000, 6000)
    _open_add_group_url()
    _type_group_name(group_name)
    _type_group_number(group_number)
    _type_context('default')
    _submit_group_form()

@step(u'When I create a group ([\w]+)$')
def when_i_create_group(step, group_name):
    _open_add_group_url()
    _type_group_name(group_name)
    _submit_group_form()

@step(u'When group ([\w]+) is removed')
def remove_group_with_name(step, group_name):
    _open_list_group_url()
    delete_button = world.browser.find_element_by_xpath("//table[@id='table-main-listing']//tr[contains(.,'%s')]//a[@title='Delete']" % group_name)
    delete_button.click()
    alert = world.browser.switch_to_alert();
    alert.accept()

@step(u'Then group (.*) is displayed in the list')
def then_group_is_displayed_in_the_list(step, group_name):
    assert _group_is_saved(group_name)

@step(u'Then group (.*) is not displayed in the list')
def then_group_is_not_displayed_in_the_list(step, group_name):
    assert not _group_is_saved(group_name)
