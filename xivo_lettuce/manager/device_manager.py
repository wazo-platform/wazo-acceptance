# -*- coding: utf-8 -*-

# Copyright (C) 2013 Avencall
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

from lettuce import world
from xivo_lettuce.common import open_url, remove_line
from xivo_lettuce import form, common
from selenium.common.exceptions import NoSuchElementException


def add_or_replace_device(info):
    delete_device(info)
    add_device_from_webi(info)


def add_device_from_webi(info):
    open_url('device', 'add')
    form.input.edit_text_field_with_id('it-device-ip', info['ip'])
    form.input.edit_text_field_with_id('it-device-mac', info['mac'])
    form.submit.submit_form()


def delete_device(info):
    search_device(info['mac'])
    try:
        remove_line(info['mac'])
    except NoSuchElementException:
        pass


def search_device(search):
    open_url('device')
    form.input.edit_text_field_with_id('it-toolbar-search', search)
    form.submit.submit_form('it-toolbar-subsearch')


def get_device_list_entry(mac_address):
    search_device(mac_address)
    try:
        line_element = world.browser.find_element_by_xpath('//table[@id="table-main-listing"]/tbody/tr[contains(@class, "sb-content") and td[@title="%s"]]' % mac_address)
    except NoSuchElementException:
        search_device('')
        raise LookupError('No device found with MAC address %s' % mac_address)

    configured_icon = line_element.find_element_by_class_name('col_configured')
    configured = 'green' in configured_icon.get_attribute('src')
    phone_number = line_element.find_element_by_class_name('col_phone_number').text
    ip_address = line_element.find_element_by_class_name('col_ip_address').text
    vendor = line_element.find_element_by_class_name('col_vendor').text
    model = line_element.find_element_by_class_name('col_model').text
    plugin = line_element.find_element_by_class_name('col_plugin').text
    return_device = {
        'configured': configured,
        'mac': mac_address,
        'phone_number': phone_number,
        'ip': ip_address,
        'vendor': vendor,
        'model': model,
        'plugin': plugin,
    }
    search_device('')

    return return_device


def type_vlan_enabled(value):
    common.go_to_tab('Advanced')
    if value == '':
        form.select.set_select_empty_value_with_id('it-config-vlan_enabled')
    else:
        form.select.set_select_field_with_id('it-config-vlan_enabled', value)
