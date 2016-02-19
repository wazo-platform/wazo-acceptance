# -*- coding: utf-8 -*-

# Copyright (C) 2013-2016 Avencall
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

from xivo_acceptance.action.webi import ldap as ldap_action_webi
from xivo_acceptance.lettuce import common


@step(u'Given there is no LDAP server "([^"]*)"$')
def given_there_is_no_ldap_server(step, search):
    common.remove_element_if_exist('LDAP server', search)


@step(u'Given there is no LDAP filter "([^"]*)"$')
def given_there_is_no_ldap_filter(step, search):
    common.remove_element_if_exist('LDAP filter', search)


@step(u'I create an LDAP server with name "([^"]*)" and host "([^"]*)"')
def i_create_an_ldap_server_with_name_1_and_host_2(step, name, host):
    ldap_action_webi.add_ldap_server(name, host)


@step(u'Given there is a LDAP server with name "([^"]*)" and with host "([^"]*)"')
def given_there_is_a_ldap_server_with_name_1_and_with_host_2(step, name, host):
    ldap_action_webi.add_or_replace_ldap_server(name=name, host=host)


@step(u'I create an LDAP filter with name "([^"]*)" and server "([^"]*)"')
def i_create_an_ldap_filter_with_name_and_server(step, name, server):
    ldap_action_webi.add_or_replace_ldap_filter(
        name=name,
        server=server,
        base_dn='dc=lan-quebec,dc=avencall,dc=com'
    )


@step(u'Given there are entries in the ldap server:')
def given_there_are_entries_in_the_ldap_server(step):
    for directory_entry in step.hashes:
        ldap_action_webi.add_or_replace_ldap_entry(directory_entry)
