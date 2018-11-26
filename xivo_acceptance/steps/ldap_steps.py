# -*- coding: utf-8 -*-
# Copyright 2013-2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from lettuce import step

from xivo_acceptance.action.webi import directory as directory_action_webi
from xivo_acceptance.action.webi import ldap as ldap_action_webi
from xivo_acceptance.helpers import cti_helper
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
    ldap_action_webi.add_or_replace_ldap_server(name='openldap-dev',
                                                host='openldap-dev.lan.wazo.io',
                                                ssl=True)
    ldap_action_webi.add_or_replace_ldap_filter(
        name='openldap-dev',
        server='openldap-dev',
        base_dn='dc=lan-quebec,dc=avencall,dc=com',
        username='cn=admin,dc=lan-quebec,dc=avencall,dc=com',
        password='superpass')


def _configure_display_filter():
    field_list = [
        (u'Nom', u'', u'name'),
        (u'Numéro', u'', u'phone')
    ]
    directory_action_webi.add_or_replace_display("Display", field_list)


def _configure_ldap_directory(ldap_filter):
    directory_action_webi.add_or_replace_directory_config({
        'name': ldap_filter,
        'type': 'LDAP filter',
        'ldap_filter': ldap_filter,
    })
    directory_action_webi.add_or_replace_directory(
        name='ldapdirectory',
        directory=ldap_filter,
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
