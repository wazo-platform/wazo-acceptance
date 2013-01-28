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
from xivo_lettuce import form


def type_ldap_name_and_host(name, host):
    input_name = world.browser.find_element_by_id('it-name', 'LDAP form  not loaded')
    input_host = world.browser.find_element_by_id('it-host', 'LDAP form  not loaded')
    input_name.send_keys(name)
    input_host.send_keys(host)


def add_ldap_server(name, host):
    common.open_url('ldapserver', 'add')
    type_ldap_name_and_host(name, host)
    form.submit.submit_form()


def add_or_replace_ldap_server(name, host):
    if common.element_is_in_list('ldapserver', name):
        common.remove_line(name)
    add_ldap_server(name, host)


def add_or_replace_ldap_filter(name, server, base_dn, username=None, password=None):
    if common.element_is_in_list('ldapfilter', name):
        common.remove_line(name)

    _add_ldap_filter(server, name, base_dn, username, password)


def _add_ldap_filter(server, name, base_dn, username=None, password=None):
    common.open_url('ldapfilter', 'add')

    _type_ldap_filter_name(name)
    _choose_ldap_server(server)

    if username and password:
        _type_username_and_password(username, password)

    _type_ldap_filter_base_dn(base_dn)

    common.go_to_tab("Attributes")

    _select_filter_display_name_field()
    _select_filter_phone_number_field()

    form.submit.submit_form()


def _select_filter_phone_number_field():
    add_button = world.browser.find_element_by_id('bt-ldapfilter-attrphonenumber-add')
    add_button.click()
    alert = world.browser.switch_to_alert()
    alert.send_keys("telephoneNumber")
    alert.accept()


def _select_filter_display_name_field():
    add_button = world.browser.find_element_by_id('bt-ldapfilter-attrdisplayname-add')
    add_button.click()
    alert = world.browser.switch_to_alert()
    alert.send_keys("sn")
    alert.accept()


def _choose_ldap_server(server):
    form.select.set_select_field_with_label_containing('LDAP Server', server)


def _type_ldap_filter_base_dn(base_dn):
    text_input = world.browser.find_element_by_label("Base DN")
    text_input.clear()
    text_input.send_keys(base_dn)


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
