# -*- coding: utf-8 -*-

# Copyright (C) 2013-2014 Avencall
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
from xivo_lettuce import common, form
from selenium.common.exceptions import NoSuchElementException


def delete_device(info):
    search_device(info['mac'])
    try:
        common.remove_line(info['mac'])
    except NoSuchElementException:
        pass


def search_device(search, by_number=False):
    common.open_url('device')
    if by_number:
        select_search_type = world.browser.find_element_by_xpath(
            '''//select[@id="it-toolbar-column"]//option[@value="number"]'''
        ).click()
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
