# -*- coding: utf-8 -*-
# Copyright (C) 2013-2014 Avencall
# Copyright (C) 2016 Proformatique Inc.
# SPDX-License-Identifier: GPL-3.0+

from lettuce.registry import world
from xivo_acceptance.lettuce import common


def search_line_number(line_number):
    common.open_url('line')
    searchbox_id = 'it-toolbar-search'
    text_input = world.browser.find_element_by_id(searchbox_id)
    text_input.clear()
    text_input.send_keys(line_number)
    submit_button = world.browser.find_element_by_id('it-toolbar-subsearch')
    submit_button.click()


def get_value_from_ipbx_infos_tab(var_name):
    common.go_to_tab('IPBX Infos')
    value_cell = world.browser.find_element_by_xpath(
        "//table"
        "//tr[td[@class = 'td-left' and text() = '%s']]"
        "//td[@class = 'td-right']"
        % var_name)
    return value_cell.text


def get_line_list_entry(search_number):
    line_tr = common.get_line(search_number)
    device_img = line_tr.find_element_by_class_name('col_identity').find_elements_by_tag_name('img')[1]
    device = 'phone-green' in device_img.get_attribute('src')
    protocol = line_tr.find_element_by_class_name('col_protocol').text.lower()
    user = line_tr.find_element_by_class_name('col_user').text
    number = line_tr.find_element_by_class_name('col_number').text
    return {
        'device': device,
        'protocol': protocol,
        'user': user,
        'number': number,
    }
