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

from lettuce import world, step
from hamcrest import assert_that, equal_to
from xivo_lettuce.xivoclient import xivoclient, xivoclient_step
from xivo_lettuce.manager_ws import context_manager_ws
from xivo_lettuce.manager import ldap_manager
from xivo_lettuce.manager import directory_manager


@step(u'When I search a transfer destination "([^"]*)"')
@xivoclient_step
def when_i_search_a_transfer_destination_1(step, group1):
    assert_that(world.xc_response, equal_to('OK'))


@step(u'Then I see transfer destinations:')
def then_i_see_transfer_destinations(step):
    for entry in step.hashes:
        assert_directory_has_entry(dict(entry))


@step(u'Then I see no transfer destinations')
@xivoclient_step
def then_i_see_no_transfer_destinations(step):
    assert_that(world.xc_response, equal_to('OK'))


@xivoclient
def assert_directory_has_entry(entry):
    assert_that(world.xc_response, equal_to('OK'))


@step(u'Given the switchboard is configured for ldap lookup with location and department$')
def given_the_switchboard_is_configured_for_ldap_lookup_with_location_and_department(step):
    context_manager_ws.add_or_replace_context('__switchboard_directory', 'Switchboard', 'internal')
    ldap_manager.add_or_replace_ldap_server('openldap-dev', 'openldap-dev.lan-quebec.avencall.com')
    ldap_manager.add_or_replace_ldap_filter('openldap-dev', 'openldap-dev',
                                            'dc=lan-quebec,dc=avencall,dc=com',
                                            'cn=admin,dc=lan-quebec,dc=avencall,dc=com',
                                            'superpass',
                                            ['cn', 'st', 'o'])

    directory_manager.add_or_replace_directory(
        'openldap',
        'ldapfilter://openldap-dev',
        'cn,telephoneNumber,st,o',
        {'name': 'cn',
         'number': 'telephoneNumber',
         'location': 'st',
         'department': 'o'}
    )
    directory_manager.add_or_replace_display(
        'switchboard',
        [('', 'status', ''),
         ('Name', 'name', '{db-name}'),
         ('Number', 'number_office', '{db-number}'),
         ('Location', '', '{db-location}'),
         ('Department', '', '{db-department}')]
    )
    directory_manager.assign_filter_and_directories_to_context(
        '__switchboard_directory',
        'switchboard',
        ['openldap']
    )


@step(u'Given the display filter "([^"]*)" exists with the following fields:')
def given_the_display_filter_group1_exists_with_the_following_fields(step, filter_name):
    field_list = []
    for line in step.hashes:
        field_list.append((line['Field title'], line['Field type'], line['Display format']))
    directory_manager.add_or_replace_display(filter_name, field_list)


@step(u'Given the context "([^"]*)" uses display "([^"]*)" with the following directories:')
def given_the_context_group1_uses_display_group2_with_the_following_directories(step, context, filter_name):
    directories = [line['Directories'] for line in step.hashes]
    directory_manager.assign_filter_and_directories_to_context(
        context, filter_name, directories
    )


@step(u'Given the switchboard is configured for ldap lookup with location$')
def given_the_switchboard_is_configured_for_ldap_lookup_with_location(step):
    context_manager_ws.add_or_replace_context('__switchboard_directory', 'Switchboard', 'internal')
    ldap_manager.add_or_replace_ldap_server('openldap-dev', 'openldap-dev.lan-quebec.avencall.com')
    ldap_manager.add_or_replace_ldap_filter('openldap-dev', 'openldap-dev',
                                            'dc=lan-quebec,dc=avencall,dc=com',
                                            'cn=admin,dc=lan-quebec,dc=avencall,dc=com',
                                            'superpass',
                                            ['cn', 'st'])

    directory_manager.add_or_replace_directory(
        'openldap',
        'ldapfilter://openldap-dev',
        'cn,telephoneNumber,st',
        {'name': 'cn',
         'number': 'telephoneNumber',
         'location': 'st'}
    )
    directory_manager.add_or_replace_display(
        'switchboard',
        [('', 'status', ''),
         ('Name', 'name', '{db-name}'),
         ('Number', 'number_office', '{db-number}'),
         ('Location', '', '{db-location}')]
    )
    directory_manager.assign_filter_and_directories_to_context(
        '__switchboard_directory',
        'switchboard',
        ['openldap']
    )


@step(u'Given the switchboard is configured for ldap lookup$')
def given_the_switchboard_is_configured_for_ldap_lookup(step):
    context_manager_ws.add_or_replace_context('__switchboard_directory', 'Switchboard', 'internal')
    ldap_manager.add_or_replace_ldap_server('openldap-dev', 'openldap-dev.lan-quebec.avencall.com')
    ldap_manager.add_or_replace_ldap_filter('openldap-dev', 'openldap-dev', 'dc=lan-quebec,dc=avencall,dc=com', 'cn=admin,dc=lan-quebec,dc=avencall,dc=com', 'superpass')
    directory_manager.add_or_replace_directory(
        'openldap',
        'ldapfilter://openldap-dev',
        'cn,telephoneNumber',
        {'name': 'cn',
         'number': 'telephoneNumber'}
    )
    directory_manager.add_or_replace_display(
        'switchboard',
        [('', 'status', ''),
         ('Name', 'name', '{db-name}'),
         ('Number', 'number_office', '{db-number}')]
    )
    directory_manager.assign_filter_and_directories_to_context(
        '__switchboard_directory',
        'switchboard',
        ['openldap']
    )


@step(u'Given the switchboard is configured for internal directory lookup')
def given_the_switchboard_is_configured_for_internal_directory_lookup(step):
    context_manager_ws.add_or_replace_context('__switchboard_directory', 'Switchboard', 'internal')
    directory_manager.add_or_replace_directory(
        'xivodir',
        'phonebook',
        'phonebook.firstname,phonebook.lastname,phonebook.displayname,phonebook.society,phonebooknumber.office.number',
        {'name': 'phonebook.displayname',
         'number': 'phonebooknumber.office.number',
         'mobile': 'phonebooknumber.mobile.number'}
    )
    directory_manager.add_or_replace_display(
        'switchboard',
        [('', 'status', ''),
         ('Name', 'name', '{db-name}'),
         ('Number', 'number_office', '{db-number}'),
         ('Number', 'number_mobile', '{db-mobile}'),
        ]
    )
    directory_manager.assign_filter_and_directories_to_context(
        '__switchboard_directory',
        'switchboard',
        ['xivodir']
    )


@step(u'Given there are entries in the ldap server:')
def given_there_are_entries_in_the_ldap_server(step):
    for directory_entry in step.hashes:
        ldap_manager.add_or_replace_entry(directory_entry)
