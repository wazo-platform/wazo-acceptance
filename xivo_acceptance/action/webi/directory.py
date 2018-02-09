# -*- coding: utf-8 -*-
# Copyright (C) 2013-2016 Avencall
# SPDX-License-Identifier: GPL-3.0+

import time

from lettuce import world
from xivo_acceptance.lettuce.form import submit, input, select
from xivo_acceptance.lettuce.form.list_pane import ListPane
from xivo_acceptance.lettuce import common


def add_or_replace_directory_config(directory):
    _remove_directory_config(directory)
    _create_directory_config(directory)


def _remove_directory_config(directory):
    common.remove_element_if_exist('directory_config', directory['name'])


def _create_directory_config(directory):
    common.open_url('directory_config', 'add')
    input.set_text_field_with_label("Directory name", directory['name'])
    select.set_select_field_with_label("Type", directory['type'])
    if 'URI' in directory:
        input.set_text_field_with_label('URI', directory['URI'])
    if 'ldap_filter' in directory:
        select.set_select_field_with_label('LDAP filter name', directory['ldap_filter'])
    submit.submit_form()


def add_directory_definition(directory):
    _add_directory(
        directory['name'],
        directory['directory'],
        directory.get('direct match', ''),
        directory.get('delimiter', ''),
        directory.get('reverse match', ''),
    )


def add_or_replace_directory(name, directory, direct_match, reverse_match, fields):
    remove_directory(name)
    _add_directory(name, directory, direct_match, None, reverse_match)
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


def remove_directory(name):
    while common.element_is_in_list('cti_directory', name):
        common.remove_line(name)

    # Work around for directory associations that aren't deleted
    common.open_url('cti_direct_directory', 'list')
    try:
        common.edit_line('default')
    except Exception:
        pass  # No default context configured
    else:
        submit.submit_form()


def _type_display_name(name):
    input.set_text_field_with_label('Name', name)


def _add_directory_fields(fields):
    time.sleep(world.timeout)  # wait for javascript to load
    for field_name, value in fields.iteritems():
        add_field(field_name, value)


def _add_directory(name, directory, direct_match, delimiter=None, reverse_match=None):
    common.open_url('cti_directory', 'add')
    input.set_text_field_with_label("Name", name)
    if delimiter:
        input.set_text_field_with_label("Delimiter", delimiter)
    input.set_text_field_with_label("Direct match", direct_match)
    if reverse_match:
        input.set_text_field_with_label("Match reverse directories", reverse_match)
    select.set_select_field_with_label("Directory", directory)


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
    lp = ListPane.from_id('contexts_services')
    lp.add(directory)


def assign_filter_and_directories_to_context(context, filter_name, directories):
    if common.element_is_in_list('cti_direct_directory', context):
        common.remove_line(context)

    common.open_url('cti_direct_directory', 'add')
    select.set_select_field_with_label("Name", context)
    select.set_select_field_with_label("Display filter", filter_name)
    for directory in directories:
        add_directory_to_context(directory)

    submit.submit_form()


def set_reverse_directories(directories):
    common.open_url('cti_reverse_directory', '')
    lp = ListPane.from_id('contexts_services')
    lp.remove_all()
    for directory in directories:
        lp.add(directory)
    submit.submit_form()
