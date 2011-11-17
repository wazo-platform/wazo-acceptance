# -*- coding: UTF-8 -*-

from lettuce.decorators import step
from lettuce.registry import world

GROUP_URL = 'service/ipbx/index.php/pbx_settings/groups/%s'


def _open_add_group_url():
    URL = GROUP_URL % '?act=add'
    world.browser.get('%s%s' % (world.url, URL))
    world.waitFor('it-groupfeatures-name', 'Group form not loaded')
    
def _open_list_group_url():
    URL = GROUP_URL % ('?act=list')
    world.browser.get('%s%s' % (world.url, URL))
    world.waitFor('table-main-listing', 'Delete button not loaded')

def _type_group_name(group_name):
    world.group_name = group_name
    input_name = world.browser.find_element_by_id('it-groupfeatures-name')
    input_name.send_keys(group_name)

def _type_group_number(group_number):
    world.group_number = group_number
    input_number = world.browser.find_element_by_id('it-groupfeatures-number')
    input_number.send_keys(group_number)

def _submit_group_form():
    return world.browser.find_element_by_id('it-submit').click()

@step(u'When I create a group (.*) with number ([0-9]+)')
def when_i_create_group_with_number(step, group_name, group_number):
    _open_add_group_url()
    _type_group_name(group_name)
    _type_group_number(group_number)
    _submit_group_form()

@step(u'When I create a group ([\w]+)$')
def when_i_create_group(step, group_name):
    _open_add_group_url()
    _type_group_name(group_name)
    _submit_group_form()

@step(u'When group with name ([\w]+) is removed')
def remove_group_with_name(step, group_name):
    _open_list_group_url()
    delete_button = world.browser.find_element_by_xpath("//table[@id='table-main-listing']//tr[contains(.,'%s')]//a[@title='Delete']" % group_name)
    delete_button.click()
    alert = world.browser.switch_to_alert();
    alert.accept()

@step(u'When group with number ([0-9]+) is removed')
def remove_group_with_number(step, group_number):
    _open_list_group_url()
    delete_button = world.browser.find_element_by_xpath("//table[@id='table-main-listing']//tr[contains(.,'%s')]//a[@title='Delete']" % group_number)
    delete_button.click()
    alert = world.browser.switch_to_alert();
    alert.accept()

@step(u'Then I should see the group (.*) in the group list')
def then_i_should_see_the_group(step, group_name):
    pass
