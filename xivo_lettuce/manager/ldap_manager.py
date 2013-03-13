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
import ldap
import ldap.modlist

LDAP_URI = 'ldap://openldap-dev.lan-quebec.avencall.com:389/'
LDAP_LOGIN = 'cn=admin,dc=lan-quebec,dc=avencall,dc=com'
LDAP_PASSWORD = 'superpass'
LDAP_USER_GROUP = 'ou=people,dc=lan-quebec,dc=avencall,dc=com'


def type_ldap_name_and_host(name, host):
    input_name = world.browser.find_element_by_id('it-name', 'LDAP form  not loaded')
    input_host = world.browser.find_element_by_id('it-host', 'LDAP form  not loaded')
    input_name.send_keys(name)
    input_host.send_keys(host)


def change_to_ssl():
    form.input.set_text_field_with_id("it-port", "636")
    form.select.set_select_field_with_id("it-securitylayer", "SSL")


def add_ldap_server(name, host, ssl=False):
    common.open_url('ldapserver', 'add')
    type_ldap_name_and_host(name, host)
    if ssl:
        change_to_ssl()
    form.submit.submit_form()


def add_or_replace_ldap_server(name, host, ssl=False):
    if common.element_is_in_list('ldapserver', name):
        common.remove_line(name)
    add_ldap_server(name, host, ssl)


def add_or_replace_ldap_filter(name, server, base_dn, username=None, password=None,
        display_fields=['cn'], number_fields=['telephoneNumber']):
    if common.element_is_in_list('ldapfilter', name):
        common.remove_line(name)

    _add_ldap_filter(server, name, base_dn, username, password, display_fields,
            number_fields)


def add_or_replace_entry(directory_entry):
    ldap_server = ldap.initialize(LDAP_URI)
    ldap_server.simple_bind(LDAP_LOGIN, LDAP_PASSWORD)

    entry_common_name = _get_entry_common_name(directory_entry)
    if _ldap_has_entry_bound(ldap_server, entry_common_name):
        entry_id = _get_entry_id(directory_entry)
        delete_entry_bound(ldap_server, entry_id)
    add_entry_bound(ldap_server, directory_entry)

    ldap_server.unbind_s()


def delete_entry_bound(ldap_server, directory_entry_id):
    directory_entry_id_encoded = directory_entry_id.encode('utf-8')
    ldap_server.delete_s(directory_entry_id_encoded)


def add_entry_bound(ldap_server, directory_entry):
    directory_entry_encoded = _encode_directory_entry(directory_entry)
    new_entry_common_name_encoded = _get_entry_common_name(directory_entry).encode('utf-8')
    new_entry_id_encoded = _get_entry_id(directory_entry).encode('utf-8')
    new_entry_attributes_encoded = {
        'objectClass': ['top', 'inetOrgPerson'],
        'givenName': directory_entry_encoded['first name'],
        'cn': new_entry_common_name_encoded,
        'sn': directory_entry_encoded['last name'],
        'telephoneNumber': directory_entry_encoded['phone'],
    }

    if 'location' in directory_entry_encoded:
        new_entry_attributes_encoded['st'] = directory_entry_encoded['location']

    if 'department' in directory_entry_encoded:
        new_entry_attributes_encoded['o'] = directory_entry_encoded['department']

    new_entry_content_encoded = ldap.modlist.addModlist(new_entry_attributes_encoded)
    ldap_server.add_s(new_entry_id_encoded, new_entry_content_encoded)


def _add_ldap_filter(server, name, base_dn, username=None, password=None,
        display_fields=['cn'], phone_fields=['telephoneNumber']):
    common.open_url('ldapfilter', 'add')

    _type_ldap_filter_name(name)
    _choose_ldap_server(server)

    if username and password:
        _type_username_and_password(username, password)

    _type_ldap_filter_base_dn(base_dn)

    common.go_to_tab("Attributes")

    for field in display_fields:
        _add_filter_display_name_field(field)

    for field in phone_fields:
        _add_filter_phone_number_field(field)

    form.submit.submit_form()


def _add_filter_phone_number_field(field):
    add_button = world.browser.find_element_by_id('bt-ldapfilter-attrphonenumber-add')
    add_button.click()
    alert = world.browser.switch_to_alert()
    alert.send_keys(field)
    alert.accept()


def _add_filter_display_name_field(field):
    add_button = world.browser.find_element_by_id('bt-ldapfilter-attrdisplayname-add')
    add_button.click()
    alert = world.browser.switch_to_alert()
    alert.send_keys(field)
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


def _get_entry_id(directory_entry):
    entry_common_name = _get_entry_common_name(directory_entry)
    return "cn=%s,ou=people,dc=lan-quebec,dc=avencall,dc=com" % entry_common_name


def _get_entry_common_name(directory_entry):
    return "%s %s" % (directory_entry['first name'], directory_entry['last name'])


def _encode_directory_entry(directory_entry):
    directory_entry_encoded = {}
    for key in directory_entry:
        directory_entry_encoded[key] = directory_entry[key].encode('utf-8')
    return directory_entry_encoded


def _ldap_has_entry_bound(ldap_server, entry_common_name):
    entry_common_name_encoded = entry_common_name.encode('utf-8')
    ldap_results = ldap_server.search_s(LDAP_USER_GROUP, ldap.SCOPE_SUBTREE, '(cn=%s)' % entry_common_name_encoded)
    if ldap_results:
        return True
    else:
        return False


def add_ldap_filter_to_phonebook(name, host):
    common.open_url('phonebook_settings')
    common.go_to_tab('LDAP filters')
    _move_filter_to_right_pane(name, host)
    form.submit.submit_form()

def _move_filter_to_right_pane(name, host):
    filter_name = "%s (%s)" % (name, host)
    form.select.set_select_field_with_id("it-ldapfilterlist", filter_name)

    button = world.browser.find_element_by_xpath("//div[@class='inout-list']/a[1]")
    button.click()
