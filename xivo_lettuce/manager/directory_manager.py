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
from xivo_lettuce.form import submit, input, select
from xivo_lettuce import common


def create_directory(directory):
    common.open_url('directory_config', 'add')
    input.set_text_field_with_label("Directory name", directory['name'])
    input.set_text_field_with_label("URI", directory['URI'])
    select.set_select_field_with_label("Type", directory['type'])
    submit.submit_form()


def add_directory_definition(directory):
    _add_directory(
        directory['name'],
        directory['URI'],
        directory['direct match'],
        directory.get('delimiter')
    )


def add_or_replace_directory(name, uri, direct_match, fields):
    if common.element_is_in_list('cti_directory', name):
        common.remove_line(name)

    _add_directory(name, uri, direct_match)
    _add_directory_fields(fields)
    submit.submit_form()


def add_or_replace_display(name, fields):
    if common.element_is_in_list('cti_display_filter', name):
        common.remove_line(name)

    common.open_url('cti_display_filter', 'add')
    _type_display_name(name)
    for title, field_type, display in fields:
        _add_display_field(title, field_type, display)
    submit.submit_form()


def _type_display_name(name):
    input.set_text_field_with_label('Name', name)


def _add_directory_fields(fields):
    for field_name, value in fields.iteritems():
        add_field(field_name, value)


def _add_directory(name, uri, direct_match, delimiter=None):
    common.open_url('cti_directory', 'add')
    input.set_text_field_with_label("Name", name)
    if delimiter:
        input.set_text_field_with_label("Delimiter", delimiter)
    input.set_text_field_with_label("Direct match", direct_match)
    select.set_select_field_with_label("URI", uri)


def add_field(fieldname, value):
    b = world.browser
    add_btn = b.find_element_by_css_selector(".sb-list table .sb-top .th-right a")
    add_btn.click()

    xpath = "//div[@class='sb-list']/table[position()=1]/tbody/tr[last()]/td[position()=%s]/input"
    fieldname_input = b.find_element_by_xpath(xpath % 1)
    fieldname_input.send_keys(fieldname)

    value_input = b.find_element_by_xpath(xpath % 2)
    value_input.send_keys(value)


def _add_display_field(title, f_type, value):
    b = world.browser
    add_btn = b.find_element_by_css_selector(".sb-list table .sb-top .th-right a")
    add_btn.click()

    xpath = "//div[@class='sb-list']/table[position()=1]/tbody/tr[last()]/td[position()=%s]/input"
    field_title = b.find_element_by_xpath(xpath % 1)
    field_title.send_keys(title)

    field_type = b.find_element_by_xpath(xpath % 2)
    field_type.send_keys(f_type)

    display_format = b.find_element_by_xpath(xpath % 4)
    display_format.send_keys(value)


def add_directory_to_context(directory):
    select.set_select_field_with_id("it-directorieslist", directory)

    right_arrow = world.browser.find_element_by_xpath("//div[@class='inout-list']/a[position()=1]")
    right_arrow.click()


def assign_filter_and_directories_to_context(context, filter_name, directories):
    if common.element_is_in_list('cti_direct_directory', context):
        common.remove_line(context)

    common.open_url('cti_direct_directory', 'add')
    select.set_select_field_with_label("Name", context)
    select.set_select_field_with_label("Display filter", filter_name)
    for directory in directories:
        add_directory_to_context(directory)

    submit.submit_form()
