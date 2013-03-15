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
    input_name = world.browser.find_element_by_id('it-name', 'LDAP form not loaded')
    input_host = world.browser.find_element_by_id('it-host', 'LDAP form not loaded')
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


def add_or_replace_ldap_filter(**args):
    opts = {
        'display_name': ['cn'],
        'phone_number': ['telephoneNumber'],
    }
    opts.update(args)

    if common.element_is_in_list('ldapfilter', opts['name']):
        common.remove_line(opts['name'])

    _add_ldap_filter(**opts)


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

    if 'city' in directory_entry_encoded:
        new_entry_attributes_encoded['l'] = directory_entry_encoded['city']

    if 'state' in directory_entry_encoded:
        new_entry_attributes_encoded['st'] = directory_entry_encoded['state']

    new_entry_content_encoded = ldap.modlist.addModlist(new_entry_attributes_encoded)
    ldap_server.add_s(new_entry_id_encoded, new_entry_content_encoded)


def _add_ldap_filter(**args):

    common.open_url('ldapfilter', 'add')

    _type_ldap_filter_name(args['name'])
    _choose_ldap_server(args['server'])

    if 'username' in args and 'password' in args:
        _type_username_and_password(args['username'], args['password'])

    _type_ldap_filter_base_dn(args['base_dn'])

    if 'custom_filter' in args:
        _type_ldap_custom_filter(args['custom_filter'])

    if 'number_type' in args:
        _select_phone_number_type(args['number_type'])

    common.go_to_tab("Attributes")

    for field in args.get('display_name', []):
        _add_filter_display_name_field(field)

    for field in args.get('phone_number', []):
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


def _select_phone_number_type(number_type):
    if number_type in ['Office', 'Home', 'Mobile', 'Fax', 'Other']:
        form.select.set_select_field_with_id("it-ldapfilter-additionaltype", number_type)
    else:
        form.select.set_select_field_with_id("it-ldapfilter-additionaltype", "Customized")
        form.input.set_text_field_with_id("it-ldapfilter-additionaltext", number_type)


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


def add_ldap_filter_to_phonebook(ldap_filter):
    common.open_url('phonebook_settings')
    common.go_to_tab('LDAP filters')
    _move_filter_to_right_pane(ldap_filter)
    form.submit.submit_form()


def _move_filter_to_right_pane(ldap_filter):
    form.select.set_select_field_with_id_containing("it-ldapfilterlist", ldap_filter)
    button = world.browser.find_element_by_xpath("//div[@class='inout-list']/a[1]")
    button.click()

def remove_all_filters_from_phonebook():
    common.open_url('phonebook_settings')
    common.go_to_tab('LDAP filters')
    _move_all_filters_to_left_pane()
    form.submit.submit_form()

def _move_all_filters_to_left_pane():
    form.select.select_all_with_id("it-ldapfilter")
    button = world.browser.find_element_by_xpath("//div[@class='inout-list']/a[2]")
    button.click()
