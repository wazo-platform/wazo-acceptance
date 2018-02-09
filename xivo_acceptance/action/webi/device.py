# -*- coding: utf-8 -*-
# Copyright (C) 2013-2014 Avencall
# Copyright (C) 2016 Proformatique Inc.
# SPDX-License-Identifier: GPL-3.0+

from lettuce import world
from xivo_acceptance.lettuce import common, form
from xivo_acceptance.lettuce.form.checkbox import Checkbox
from selenium.common.exceptions import NoSuchElementException


def search_device(search, by_number=False):
    query = {'search': '%s' % search,
             'search_column': 'number' if by_number else ''}
    common.open_url('device', 'search', query)


def get_device_list_entry(mac_address):
    search_device(mac_address)
    try:
        line_element = world.browser.find_element_by_xpath('//table[@id="table-main-listing"]/tbody/tr[contains(@class, "sb-content") and td[@title="%s"]]' % mac_address)
    except NoSuchElementException:
        search_device('')
        raise LookupError('No device found with MAC address %s' % mac_address)

    configured_icon = line_element.find_element_by_class_name('col_configured')
    configured = 'green' in configured_icon.get_attribute('src')
    ip_address = line_element.find_element_by_class_name('col_ip_address').text
    vendor = line_element.find_element_by_class_name('col_vendor').text
    model = line_element.find_element_by_class_name('col_model').text
    plugin = line_element.find_element_by_class_name('col_plugin').text
    return_device = {
        'configured': configured,
        'mac': mac_address,
        'ip': ip_address,
        'vendor': vendor,
        'model': model,
        'plugin': plugin,
    }
    search_device('')

    return return_device


def type_input(field, value):
    form.input.edit_text_field_with_id('it-device-%s' % field, value)


def type_select(field, value):
    if value == '':
        form.select.set_select_empty_value_with_id('it-device-%s' % field)
    else:
        form.select.set_select_field_with_id('it-device-%s' % field, value)


def is_switchboard_enabled():
    switchboard_element = world.browser.find_element_by_id('it-device-switchboard-id')
    return switchboard_element.is_enabled()


def is_switchboard_checked():
    switchboard_element = world.browser.find_element_by_id('it-device-switchboard-id')
    return switchboard_element.is_selected()


def select_plugin(plugin_name):
    form.set_select_field_with_id_containing('it-device-plugin', plugin_name)


def check_switchboard():
    switchboard_element = world.browser.find_element_by_id('it-device-switchboard-id')
    checkbox = Checkbox(switchboard_element)
    checkbox.check()
