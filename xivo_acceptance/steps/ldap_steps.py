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

from xivo_acceptance.action.webi import directory as directory_action_webi
from xivo_acceptance.action.webi import ldap as ldap_action_webi
from xivo_acceptance.helpers import cti_helper
from xivo_acceptance.lettuce import assets
from xivo_acceptance.lettuce import common
from xivo_acceptance.lettuce import sysutils


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


@step(u"Given there's an LDAP server configured for reverse lookup with entries:")
def given_there_s_an_ldap_server_configured_for_reverse(step):
    ldap_filter = 'openldap-dev'
    _configure_ldap_ssl(step)
    for directory_entry in step.hashes:
        ldap_action_webi.add_or_replace_ldap_entry(directory_entry)
    _configure_display_filter()
    _configure_ldap_directory(ldap_filter)
    _add_directory_to_direct_directories()
    directory_action_webi.set_reverse_directories(['ldapdirectory'])
    cti_helper.restart_server()


def _configure_ldap_ssl(step):
    _copy_ca_certificate()
    _configure_ca_certificate()
    ldap_action_webi.add_or_replace_ldap_server(name='openldap-dev',
                                                host='openldap-dev.lan-quebec.avencall.com',
                                                ssl=True)
    ldap_action_webi.add_or_replace_ldap_filter(
        name='openldap-dev',
        server='openldap-dev',
        base_dn='dc=lan-quebec,dc=avencall,dc=com',
        username='cn=admin,dc=lan-quebec,dc=avencall,dc=com',
        password='superpass')


def _copy_ca_certificate():
    assets.copy_asset_to_server("ca-certificates.crt", "/etc/ssl/certs/ca-certificates.crt")


def _configure_ca_certificate():
    command = ['grep', 'TLS_CACERT', '/etc/ldap/ldap.conf']
    output = sysutils.output_command(command)
    if not output.strip():
        command = ["echo 'TLS_CACERT /etc/ssl/certs/ca-certificates.crt' >> /etc/ldap/ldap.conf"]
        sysutils.send_command(command)


def _configure_display_filter():
    field_list = [
        (u'Nom', u'', u'name'),
        (u'Numéro', u'', u'phone')
    ]
    directory_action_webi.add_or_replace_display("Display", field_list)


def _configure_ldap_directory(ldap_filter):
    directory_action_webi.add_or_replace_directory(
        name='ldapdirectory',
        uri='ldapfilter://%s' % ldap_filter,
        direct_match='sn,givenName,telephoneNumber',
        reverse_match='telephoneNumber',
        fields={
            'firstname': '{givenName}',
            'lastname': '{sn}',
            'name': '{givenName} {sn}',
            'phone': '{telephoneNumber}',
            'reverse': '{givenName}',
        },
    )


def _add_directory_to_direct_directories(directories=['ldapdirectory']):
    directory_action_webi.assign_filter_and_directories_to_context(
        'default',
        'Display',
        directories
    )
