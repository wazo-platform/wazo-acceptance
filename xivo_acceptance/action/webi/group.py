# -*- coding: utf-8 -*-
# Copyright (C) 2013-2014 Avencall
# SPDX-License-Identifier: GPL-3.0-or-later

from lettuce import world
from xivo_acceptance.lettuce import common


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


def remove_group_with_name(group_name):
    common.remove_element_if_exist('group', group_name)
    common.wait_until(group_is_no_longer_in_list, group_name, tries=5)


def group_is_no_longer_in_list(group_name):
    return common.find_line(group_name) is None
