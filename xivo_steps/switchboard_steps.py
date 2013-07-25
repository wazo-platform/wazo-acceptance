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

from lettuce import step
from hamcrest import assert_that, equal_to
from xivo_lettuce.manager_ws import context_manager_ws
from xivo_lettuce.manager import ldap_manager, cti_client_manager
from xivo_lettuce.manager import directory_manager
from xivo_lettuce.manager import user_manager
from xivo_lettuce.manager import queue_manager
from xivo_lettuce import func


@step(u'Given the switchboard is configured for ldap lookup with location and department$')
def given_the_switchboard_is_configured_for_ldap_lookup_with_location_and_department(step):
    context_manager_ws.add_or_replace_context('__switchboard_directory', 'Switchboard', 'internal')
    step.given('Given the LDAP server is configured and active')
    ldap_manager.add_or_replace_ldap_filter(
        name='openldap-dev',
        server='openldap-dev',
        base_dn='dc=lan-quebec,dc=avencall,dc=com',
        username='cn=admin,dc=lan-quebec,dc=avencall,dc=com',
        password='superpass',
        display_name=['cn', 'st', 'o'])

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
        [('Icon', 'status', ''),
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


@step(u'Given the switchboard is configured for ldap lookup with location$')
def given_the_switchboard_is_configured_for_ldap_lookup_with_location(step):
    context_manager_ws.add_or_replace_context('__switchboard_directory', 'Switchboard', 'internal')
    step.given('Given the LDAP server is configured and active')
    ldap_manager.add_or_replace_ldap_server('openldap-dev', 'openldap-dev.lan-quebec.avencall.com')
    ldap_manager.add_or_replace_ldap_filter(
        name='openldap-dev',
        server='openldap-dev',
        base_dn='dc=lan-quebec,dc=avencall,dc=com',
        username='cn=admin,dc=lan-quebec,dc=avencall,dc=com',
        password='superpass',
        display_name=['cn', 'st'])

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
        [('Icon', 'status', ''),
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
    step.given('Given the LDAP server is configured and active')
    ldap_manager.add_or_replace_ldap_filter(
        name='openldap-dev',
        server='openldap-dev',
        base_dn='dc=lan-quebec,dc=avencall,dc=com',
        username='cn=admin,dc=lan-quebec,dc=avencall,dc=com',
        password='superpass')

    directory_manager.add_or_replace_directory(
        'openldap',
        'ldapfilter://openldap-dev',
        'cn,telephoneNumber',
        {'name': 'cn',
         'number': 'telephoneNumber'}
    )
    directory_manager.add_or_replace_display(
        'switchboard',
        [('Icon', 'status', ''),
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
        'xivodirswitchboard',
        'phonebook',
        'phonebook.firstname,phonebook.lastname,phonebook.displayname,phonebook.society,phonebooknumber.office.number',
        {'name': 'phonebook.displayname',
         'number': 'phonebooknumber.office.number',
         'mobile': 'phonebooknumber.mobile.number'}
    )
    directory_manager.add_or_replace_display(
        'switchboard',
        [('Icon', 'status', ''),
         ('Name', 'name', '{db-name}'),
         ('Number', 'number_office', '{db-number}'),
         ('Number', 'number_mobile', '{db-mobile}')]
    )
    directory_manager.assign_filter_and_directories_to_context(
        '__switchboard_directory',
        'switchboard',
        ['xivodirswitchboard']
    )


@step(u'Given the display filter "([^"]*)" exists with the following fields:')
def given_the_display_filter_group1_exists_with_the_following_fields(step, filter_name):
    field_list = []
    for line in step.hashes:
        field_list.append((line['Field title'], line['Field type'], line['Display format']))
    directory_manager.add_or_replace_display(filter_name, field_list)


@step(u'Given there are entries in the ldap server:')
def given_there_are_entries_in_the_ldap_server(step):
    for directory_entry in step.hashes:
        ldap_manager.add_or_replace_entry(directory_entry)


@step(u'Given the user "([^"]*)" is configured for switchboard use')
def given_the_user_group1_is_configured_for_switchboard_use(step, user):
    user_manager.switchboard_config_for_user(user)


@step(u'Given there is a switchboard configured as:')
def given_there_is_a_switchboard_configured_as(step):
    for config in step.hashes:
        queue_manager.add_or_replace_switchboard_queue(
            config['incalls queue name'],
            config['incalls queue number'],
            config['incalls queue context'],
            config['agents'])

        queue_manager.add_or_replace_switchboard_hold_queue(
            config['hold calls queue name'],
            config['hold calls queue number'],
            config['hold calls queue context'])


@step(u'When I search a transfer destination "([^"]*)"')
def when_i_search_a_transfer_destination_1(step, search):
    cti_client_manager.set_search_for_directory(search)


@step(u'Then I see transfer destinations:')
def then_i_see_transfer_destinations(step):
    res = cti_client_manager.get_switchboard_infos()
    assert_res = func.has_subsets_of_dicts(step.hashes, res['return_value']['content'])
    assert_that(assert_res, equal_to(True))


@step(u'Then I see no transfer destinations')
def then_i_see_no_transfer_destinations(step):
    res = cti_client_manager.get_switchboard_infos()
    assert_that(res['return_value']['content'], equal_to([]))
