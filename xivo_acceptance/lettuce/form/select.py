# -*- coding: utf-8 -*-

# Copyright (C) 2013-2014 Avencall
# Copyright (C) 2016 Proformatique Inc.
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
from selenium.webdriver.support.select import Select


def set_select_field_with_label(field_label, value):
    select_input = world.browser.find_element_by_label(field_label)
    Select(select_input).select_by_visible_text(value)


def set_select_field_with_id(field_id, value):
    select_input = world.browser.find_element_by_id(field_id)
    Select(select_input).select_by_visible_text(value)


def set_select_field_with_id_containing(field_id, filter_string):
    select_input = Select(world.browser.find_element_by_id(field_id))
    _select_option_containing(filter_string, select_input)


def set_select_field_with_label_containing(label, filter_string):
    select_input = Select(world.browser.find_element_by_label(label))
    _select_option_containing(filter_string, select_input)


def _select_option_containing(filter_string, select_input):
    options = select_input.options
    for option in options:
        if filter_string in option.text:
            select_input.select_by_value(option.get_attribute('value'))
