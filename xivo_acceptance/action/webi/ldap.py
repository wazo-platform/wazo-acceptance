# -*- coding: utf-8 -*-
# Copyright (C) 2013-2014 Avencall
# SPDX-License-Identifier: GPL-3.0-or-later

import time

from lettuce.registry import world
from selenium.common.exceptions import NoSuchElementException

from xivo_acceptance.lettuce import common
from xivo_acceptance.lettuce import form
from xivo_acceptance.lettuce import ldap_utils


def type_ldap_name_and_host(name, host, port):
    form.input.set_text_field_with_id("it-name", name)
    form.input.set_text_field_with_id("it-host", host)
    form.input.set_text_field_with_id("it-port", str(port))


def change_to_ssl():
    form.input.set_text_field_with_id("it-port", "636")
    form.select.set_select_field_with_id("it-securitylayer", "SSL")


def add_ldap_server(name, host, ssl=False, port=389):
    common.open_url('ldapserver', 'add')
    type_ldap_name_and_host(name, host, port)
    if ssl:
        change_to_ssl()
    form.submit.submit_form()


def add_or_replace_ldap_server(name, host, ssl=False, port=389):
    if common.element_is_in_list('ldapserver', name):
        common.remove_line(name)
    time.sleep(1)
    add_ldap_server(name, host, ssl=ssl, port=port)


def add_or_replace_ldap_filter(**args):
    if common.element_is_in_list('ldapfilter', args['name']):
        common.remove_line(args['name'])

    _add_ldap_filter(**args)


def add_or_replace_ldap_entry(directory_entry):
    entry = _convert_directory_entry(directory_entry)
    ldap_utils.add_or_replace_ldap_entry(entry)


def _convert_directory_entry(directory_entry):
    new_entry_common_name = _get_entry_common_name(directory_entry)

    new_entry_attributes = {
        'objectClass': ['top', 'inetOrgPerson'],
        'givenName': directory_entry['first name'],
        'cn': new_entry_common_name,
        'sn': directory_entry['last name'],
        'telephoneNumber': directory_entry['phone'],
    }

    if 'location' in directory_entry:
        new_entry_attributes['st'] = directory_entry['location']

    if 'department' in directory_entry:
        new_entry_attributes['o'] = directory_entry['department']

    if 'city' in directory_entry:
        new_entry_attributes['l'] = directory_entry['city']

    if 'state' in directory_entry:
        new_entry_attributes['st'] = directory_entry['state']

    if 'mobile' in directory_entry:
        new_entry_attributes['mobile'] = directory_entry['mobile']

    if 'email' in directory_entry:
        new_entry_attributes['mail'] = directory_entry['email']

    return new_entry_attributes


def _get_entry_common_name(directory_entry):
    return "%s %s" % (directory_entry['first name'], directory_entry['last name'])


def _add_ldap_filter(**args):
    common.open_url('ldapfilter', 'add')

    _type_ldap_filter_name(args['name'])
    _choose_ldap_server(args['server'])

    if 'username' in args and 'password' in args:
        _type_username_and_password(args['username'], args['password'])

    _type_ldap_filter_base_dn(args['base_dn'])

    if 'custom_filter' in args:
        _type_ldap_custom_filter(args['custom_filter'])

    form.submit.submit_form()


def _choose_ldap_server(server):
    form.select.set_select_field_with_label_containing('LDAP Server', server)


def _type_ldap_filter_base_dn(base_dn):
    text_input = world.browser.find_element_by_label("Base DN")
    text_input.clear()
    text_input.send_keys(base_dn)


def _type_ldap_custom_filter(custom_filter):
    form.input.set_text_field_with_id("it-ldapfilter-filter", custom_filter)


def _type_ldap_filter_name(name):
    text_input = world.browser.find_element_by_label("Name")
    text_input.clear()
    text_input.send_keys(name)


def _type_username_and_password(username, password):
    text_input = world.browser.find_element_by_label("User")
    text_input.clear()
    text_input.send_keys(username)

    text_input = world.browser.find_element_by_label("Password")
    text_input.clear()
    text_input.send_keys(password)
