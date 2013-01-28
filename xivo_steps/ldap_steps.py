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

from lettuce import step, world
from xivo_lettuce.manager import ldap_manager
from xivo_lettuce import common


@step(u'I create an LDAP server with name "([^"]*)" and host "([^"]*)"')
def i_create_an_ldap_server_with_name_1_and_host_2(step, name, host):
    ldap_manager.add_ldap_server(name, host)


@step(u'Given there is a LDAP server with name "([^"]*)" and with host "([^"]*)"')
def given_there_is_a_ldap_server_with_name_1_and_with_host_2(step, name, host):
    ldap_manager.add_or_replace_ldap_server(name, host)


@step(u'I create an LDAP filter with name "([^"]*)" and server "([^"]*)"')
def i_create_an_ldap_filter_with_name_and_server(step, name, server):
    ldap_manager.add_or_replace_ldap_filter(
        'openldap-dev',
        'openldap-dev',
        'dc=lan-quebec,dc=avencall,dc=com'
    )


@step(u'Given there exist an LDAP entry "([^"]*)" on ldap server "([^"]*)"')
def given_there_exist_an_ldap_entry_on_ldap_server(step, dn, server):
    commands = ['slapcat | grep "cn=foobar state,ou=people,dc=lan-quebec,dc=avencall,dc=com"']
    ret = world.ssh_client_xivo.out_call(commands)
    assert False, ret


@step(u'When I search "([^"]*)" on an aastra phone')
def when_i_search_group1_on_an_aastra_phone(step, group1):
    assert False, 'This step must be implemented'


@step(u'Then result "([^"]*)" is present')
def then_result_group1_is_present(step, group1):
    assert False, 'This step must be implemented'


@step(u'Given there is an LDAP filter with name "([^"]*)" and with server "([^"]*)"')
def given_there_is_an_ldap_filter_with_name_and_with_server(step, name, server):
    if common.element_is_not_in_list('ldapfilter', name):
        step.given('I create an LDAP filter with name "%s" and server "%s"' % (name, server))
