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


def set_text_field_with_label(field_label, value):
    text_input = world.browser.find_element_by_label(field_label)
    text_input.clear()
    text_input.send_keys(value)


def set_text_field_with_id(field_id, value):
    text_input = world.browser.find_element_by_id(field_id)
    text_input.clear()
    text_input.send_keys(value)


def edit_text_field_with_id(field_id, new_value):
    input_field = world.browser.find_element_by_id(field_id)
    input_field.clear()
    input_field.send_keys(new_value)
