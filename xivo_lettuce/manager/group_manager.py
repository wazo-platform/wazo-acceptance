# -*- coding: utf-8 -*-

from lettuce.registry import world
from xivo_lettuce.common import *

WS = get_webservices('group')


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
    remove_element_if_exist('group', group_number)


def remove_group_with_name(group_name):
    remove_element_if_exist('group', group_name)


def delete_all_group():
    WS.clear()
