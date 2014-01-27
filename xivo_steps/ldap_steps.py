# -*- coding: utf-8 -*-

# Copyright (C) 2013-2014 Avencall
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
from xivo_acceptance.action.webi import directory as directory_action_webi
from xivo_lettuce import assets, common, sysutils, ldap_utils
from xivo_acceptance.helpers import cti_helper


def _check_ldap_is_up():
    if not ldap_utils.is_ldap_booted():
        ldap_utils.boot_ldap_server()
    ldap_utils.start_ldap_server()


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
    ldap_action_webi.add_or_replace_ldap_server(name, host)


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
        ldap_action_webi.add_or_replace_entry(directory_entry)


@step(u'Given the CTI directory definition is configured for LDAP searches using the ldap filter "([^"]*)"')
def given_the_cti_directory_definition_is_configured_for_ldap_searches_using_the_ldap_filter(step, ldap_filter):
    _configure_display_filter()
    _configure_ldap_directory(ldap_filter)
    _add_directory_to_direct_directories()
    cti_helper.restart_server()


@step(u"Given there's an LDAP server configured for reverse lookup with entries:")
def given_there_s_an_ldap_server_configured_for_reverse(step):
    ldap_filter = 'openldap-dev'
    given_the_ldap_server_is_configured_for_ssl_connections(step)
    for directory_entry in step.hashes:
        ldap_action_webi.add_or_replace_entry(directory_entry)
    _configure_display_filter()
    _configure_ldap_directory(ldap_filter)
    _add_directory_to_direct_directories()
    given_the_cti_directory_definition_is_configured_for_ldap_searches_using_the_ldap_filter('openldap-dev')
    directory_action_webi.set_reverse_directories([ldap_filter])
    cti_helper.restart_server()


@step(u'Given the LDAP server is configured for SSL connections')
def given_the_ldap_server_is_configured_for_ssl_connections(step):
    _copy_ca_certificate()
    _configure_ca_certificate()
    ldap_action_webi.add_or_replace_ldap_server('openldap-dev', 'openldap-dev.lan-quebec.avencall.com', True)
    ldap_action_webi.add_or_replace_ldap_filter(
        name='openldap-dev',
        server='openldap-dev',
        base_dn='dc=lan-quebec,dc=avencall,dc=com',
        username='cn=admin,dc=lan-quebec,dc=avencall,dc=com',
        password='superpass',
        display_name=['cn', 'st', 'givenName'],
        phone_number=['telephoneNumber'])
    ldap_action_webi.add_ldap_filter_to_phonebook('openldap-dev')
    _check_ldap_is_up()


def _copy_ca_certificate():
    assets.copy_asset_to_server("ca-certificates.crt", "/etc/ssl/certs/ca-certificates.crt")


def _configure_ca_certificate():
    command = ['grep', 'TLS_CACERT', '/etc/ldap/ldap.conf']
    output = sysutils.output_command(command)
    if not output.strip():
        command = ["echo 'TLS_CACERT /etc/ssl/certs/ca-certificates.crt' >> /etc/ldap/ldap.conf"]
        sysutils.send_command(command)


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

        ldap_action_webi.add_or_replace_ldap_filter(**options)


@step(u'Given the ldap filter "([^"]*)" has been added to the phonebook')
def given_the_ldap_filter_group1_has_been_added_to_the_phonebook(step, ldap_filter):
    ldap_action_webi.add_ldap_filter_to_phonebook(ldap_filter)


@step(u'Given there are no LDAP filters configured in the phonebook')
def given_there_are_no_ldap_filters_configured_in_the_phonebook(step):
    ldap_action_webi.remove_all_filters_from_phonebook()


@step(u'Given there is a user with common name "([^"]*)" and password "([^"]*)" on the ldap server')
def given_there_is_a_user_with_common_name_group1_and_password_group2_on_the_ldap_server(step, common_name, password):
    entry = {
        'objectClass': ['top', 'inetOrgPerson'],
        'cn': common_name,
        'sn': common_name,
        'userPassword': ldap_utils.generate_ldap_password(password)
    }

    ldap_utils.add_or_replace_entry(entry)


@step(u'Given the LDAP server is configured and active')
def given_the_ldap_server_is_configured_and_active(step):
    ldap_action_webi.add_or_replace_ldap_server('openldap-dev', 'openldap-dev.lan-quebec.avencall.com')
    _check_ldap_is_up()


@step(u'When the LDAP service is stopped')
def when_the_ldap_service_is_stopped(step):
    ldap_utils.stop_ldap_server()


@step(u'When I shut down the LDAP server')
def when_i_shut_down_the_ldap_server(step):
    ldap_utils.shutdown_ldap_server()


def _configure_display_filter():
    field_list = [
        (u'Nom', u'', u'{db-firstname} {db-lastname}'),
        (u'Numéro', u'', u'{db-phone}')
    ]
    directory_action_webi.add_or_replace_display("Display", field_list)


def _configure_ldap_directory(ldap_filter):
    directory_action_webi.add_or_replace_directory(
        name='ldapdirectory',
        uri='ldapfilter://%s' % ldap_filter,
        direct_match='sn,givenName,telephoneNumber',
        fields={'firstname': 'givenName',
                'lastname': 'sn',
                'phone': 'telephoneNumber'},
    )


def _add_directory_to_direct_directories(directories=['ldapdirectory']):
    directory_action_webi.assign_filter_and_directories_to_context(
        'default',
        'Display',
        directories
    )
