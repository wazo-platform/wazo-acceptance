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
from xivo_lettuce import common, assets, sysutils


@step(u'I create an LDAP server with name "([^"]*)" and host "([^"]*)"')
def i_create_an_ldap_server_with_name_1_and_host_2(step, name, host):
    ldap_manager.add_ldap_server(name, host)


@step(u'Given there is a LDAP server with name "([^"]*)" and with host "([^"]*)"')
def given_there_is_a_ldap_server_with_name_1_and_with_host_2(step, name, host):
    ldap_manager.add_or_replace_ldap_server(name, host)


@step(u'I create an LDAP filter with name "([^"]*)" and server "([^"]*)"')
def i_create_an_ldap_filter_with_name_and_server(step, name, server):
    ldap_manager.add_or_replace_ldap_filter(
        name=name,
        server=server,
        base_dn='dc=lan-quebec,dc=avencall,dc=com'
    )


@step(u'Given there exist an LDAP entry "([^"]*)" on ldap server "([^"]*)"')
def given_there_exist_an_ldap_entry_on_ldap_server(step, dn, server):
    commands = ['slapcat | grep "cn=foobar state,ou=people,dc=lan-quebec,dc=avencall,dc=com"']
    ret = world.ssh_client_xivo.out_call(commands)
    assert False, ret


@step(u'Given there is an LDAP filter with name "([^"]*)" and with server "([^"]*)"')
def given_there_is_an_ldap_filter_with_name_and_with_server(step, name, server):
    if common.element_is_not_in_list('ldapfilter', name):
        step.given('I create an LDAP filter with name "%s" and server "%s"' % (name, server))


@step(u'Given the LDAP server is configured for SSL connections')
def given_the_ldap_server_is_configured_for_ssl_connections(step):
    _copy_ca_certificate()
    _configure_ca_certificate()
    ldap_manager.add_or_replace_ldap_server('openldap-dev', 'openldap-dev.lan-quebec.avencall.com', True)
    ldap_manager.add_or_replace_ldap_filter(
        name='openldap-dev',
        server='openldap-dev',
        base_dn='dc=lan-quebec,dc=avencall,dc=com',
        username='cn=admin,dc=lan-quebec,dc=avencall,dc=com',
        password='superpass',
        display_name=['cn', 'st', 'givenName'],
        phone_number=['telephoneNumber'])
    ldap_manager.add_ldap_filter_to_phonebook('openldap-dev')


def _copy_ca_certificate():
    assets.copy_asset_to_server("ca-certificates.crt", "/etc/ssl/certs/ca-certificates.crt")


def _configure_ca_certificate():
    command = ['grep', 'TLS_CACERT', '/etc/ldap/ldap.conf']
    output = sysutils.output_command(command)
    if not output.strip():
        command = ["echo 'TLS_CACERT /etc/ssl/certs/ca-certificates.crt' >> /etc/ldap/ldap.conf"]
        sysutils.send_command(command)


@step(u'^Given the LDAP server is configured$')
def given_the_ldap_server_is_configured(step):
    ldap_manager.add_or_replace_ldap_server('openldap-dev', 'openldap-dev.lan-quebec.avencall.com')


@step(u'Given there are the following ldap filters:')
def given_there_are_the_following_ldap_filters(step):
    for ldap_filter in step.hashes:
        options = dict(
            name=ldap_filter['name'],
            server=ldap_filter['server'],
            base_dn=ldap_filter['base dn'],
            username=ldap_filter['username'],
            password=ldap_filter['password'])

        if 'display name' in ldap_filter:
            options['display_name'] = ldap_filter['display name'].split(',')

        if 'phone number' in ldap_filter:
            options['phone_number'] = ldap_filter['phone number'].split(',')

        if 'filter' in ldap_filter:
            options['custom_filter'] = ldap_filter['filter']

        if 'phone number type' in ldap_filter:
            options['number_type'] = ldap_filter['phone number type']

        ldap_manager.add_or_replace_ldap_filter(**options)

@step(u'Given the ldap filter "([^"]*)" has been added to the phonebook')
def given_the_ldap_filter_group1_has_been_added_to_the_phonebook(step, ldap_filter):
    ldap_manager.add_ldap_filter_to_phonebook(ldap_filter)

@step(u'Given there are no LDAP filters configured in the phonebook')
def given_there_are_no_ldap_filters_configured_in_the_phonebook(step):
    ldap_manager.remove_all_filters_from_phonebook()
