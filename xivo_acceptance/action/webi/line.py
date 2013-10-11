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

from lettuce.registry import world
from xivo_lettuce import common


def search_line_number(line_number):
    common.open_url('line')
    searchbox_id = 'it-toolbar-search'
    text_input = world.browser.find_element_by_id(searchbox_id)
    text_input.clear()
    text_input.send_keys(line_number)
    submit_button = world.browser.find_element_by_id('it-toolbar-subsearch')
    submit_button.click()


def unsearch_line():
    common.open_url('line')
    searchbox_id = 'it-toolbar-search'
    text_input = world.browser.find_element_by_id(searchbox_id)
    text_input.clear()
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
