# -*- coding: utf-8 -*-
# Copyright 2013-2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

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
