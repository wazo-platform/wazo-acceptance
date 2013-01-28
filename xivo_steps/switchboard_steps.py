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
from xivo_lettuce import form


@step(u'When I search a transfer destination "([^"]*)"')
@xivoclient_step
def when_i_search_a_transfer_destination_1(step, group1):
    assert_that(world.xc_response, equal_to('OK'))


@step(u'Then I see transfer destinations:')
def then_i_see_transfer_destinations(step):
    for entry in step.hashes:
        assert_directory_has_entry(entry['display_name'], entry['phone'])


@step(u'Then I see no transfer destinations')
@xivoclient_step
def then_i_see_no_transfer_destinations(step):
    assert_that(world.xc_response, equal_to('OK'))


@xivoclient
def assert_directory_has_entry(name, phone_number):
    assert_that(world.xc_response, equal_to('OK'))


@step(u'Given the switchboard is configured for ldap lookup')
def given_the_switchboard_is_configured_for_ldap_lookup(step):
    context_manager_ws.add_or_replace_context('__switchboard_directory', 'Switchboard', 'internal')
    ldap_manager.add_or_replace_ldap_server('openldap-dev', 'openldap-dev.lan-quebec.avencall.com')
    ldap_manager.add_or_replace_ldap_filter('openldap-dev', 'openldap-dev', 'cn=admin,dc=lan-quebec,dc=avencall,dc=com', 'superpass', 'dc=lan-quebec,dc=avencall,dc=com')
    directory_manager.add_or_replace_directory(
        'openldap',
        'ldapfilter://openldap-dev',
        'name,number',
        {'name': 'cn',
         'number': 'telephoneNumber'}
    )
    directory_manager.add_or_replace_display(
        'switchboard',
        {'name': '{db-name}',
         'number': '{db-number}'}
    )
    directory_manager.assign_filter_and_directories_to_context(
        '__switchboard_directory',
        'switchboard',
        ['openldap']
    )
