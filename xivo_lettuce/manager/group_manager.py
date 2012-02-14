# -*- coding: utf-8 -*-

from lettuce.registry import world
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException
from webservices.webservices import WebServicesFactory
from xivo_lettuce.common import *

GROUP_URL = '/service/ipbx/index.php/pbx_settings/groups/%s'
WS = WebServicesFactory('ipbx/pbx_settings/groups')


def open_add_group_url():
    URL = GROUP_URL % '?act=add'
    world.browser.get('%s%s' % (world.url, URL))
    world.browser.find_element_by_id('it-groupfeatures-name', 'Group form not loaded')


def open_list_group_url():
    URL = GROUP_URL % ('?act=list')
    world.browser.get('%s%s' % (world.url, URL))
    world.browser.find_element_by_name('fm-group-list', 'Group list not loaded')


def type_group_name(group_name):
    world.browser.find_element_by_id('it-groupfeatures-name', 'Group form not loaded')
    world.group_name = group_name
    input_name = world.browser.find_element_by_id('it-groupfeatures-name')
    input_name.send_keys(group_name)


def type_group_number(group_number):
    world.browser.find_element_by_id('it-groupfeatures-number', 'Group form not loaded')
    world.group_number = group_number
    input_number = world.browser.find_element_by_id('it-groupfeatures-number')
    input_number.send_keys(group_number)


def type_context(context):
    select_context = world.browser.find_element_by_xpath(
        '//select[@id="it-groupfeatures-context"]//option[@value="%s"]' % context)
    select_context.click()


def remove_group_with_number(group_number):
    open_list_group_url()
    try:
        remove_line(group_number)
    except NoSuchElementException:
        pass


def remove_group_with_name(group_name):
    open_list_group_url()
    try:
        remove_line(group_name)
    except NoSuchElementException, ElementNotVisibleException:
        pass


def group_is_saved(group_name):
    open_list_group_url()
    try:
        group = find_line(group_name)
        return group is not None
    except NoSuchElementException:
        return False


def delete_all_group():
    WS.clear()
