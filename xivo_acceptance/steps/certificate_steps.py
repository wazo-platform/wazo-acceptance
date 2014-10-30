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

import datetime

from hamcrest import assert_that, equal_to
from lettuce import step, world

from xivo_acceptance.helpers import asterisk_helper
from xivo_acceptance.lettuce import common, form, logs
from xivo_acceptance.lettuce.form.checkbox import Checkbox


def create_or_replace_certificate(info):
    common.remove_all_elements('certificat', info['name'])

    common.open_url('certificat', 'add')

    input_name = world.browser.find_element_by_id('it-name')
    input_name.send_keys(info['name'])

    if 'autosigned' in info:
        checked = info['autosigned'] == "yes"
        Checkbox.from_id('it-autosigned').set_checked(checked)

    if 'certificate authority' in info:
        checked = info['certificate authority'] == "yes"
        Checkbox.from_id('it-is_ca').set_checked(checked)

    input_date = world.browser.find_element_by_id('it-validity-end')
    input_date.clear()

    date = datetime.datetime.now()
    if info['valid date in the future'] == "yes":
        date += datetime.timedelta(days=31)
    else:
        date -= datetime.timedelta(days=1)

    input_date.send_keys(date.strftime("%m/%d/%Y"))

    input_email = world.browser.find_element_by_id('it-subject-emailAddress')
    input_email.clear()
    input_email.send_keys(info['email'])


def insert_hostname_into_form():
    command = ['hostname', '-f']
    hostname = world.ssh_client_xivo.out_call(command).strip()

    input_cn = world.browser.find_element_by_id("it-subject-CN")
    input_cn.send_keys(hostname)


def update_sip_configuration(info):
    common.open_url('general_sip')
    common.go_to_tab('Security')

    checked = info['allow tls connections'] == "yes"
    Checkbox.from_label("Allow TLS connections").set_checked(checked)

    form.input.set_text_field_with_label("Listening address", info['listening address'])
    form.select.set_select_field_with_label("Server certificate", info['server certificate'])
    form.select.set_select_field_with_label("CA certificate", info['ca certificate'])
    form.submit.submit_form()


@step(u'When I create a certificate with the following invalid info:')
def when_i_create_a_certificate_with_the_following_invalid_info(step):
    for info in step.hashes:
        create_or_replace_certificate(info)
        form.submit.submit_form_with_errors()


@step(u'When I create a certificate with following valid info:')
def when_i_create_a_certificate_with_following_valid_info(step):
    for info in step.hashes:
        create_or_replace_certificate(info)
        form.submit.submit_form()


@step(u'I create a certificate with following valid info and the server\'s hostname as common name:$')
def i_create_a_certificate_with_following_valid_info_and_the_server_s_hostname_as_common_name(step):
    for info in step.hashes:
        create_or_replace_certificate(info)
        insert_hostname_into_form()
        form.submit.submit_form()


@step(u'When I enable the following options for the SIP Protocol:')
def when_i_enable_the_following_options_for_the_sip_protocol(step):
    for info in step.hashes:
        update_sip_configuration(info)


@step(u'Then SIP tls connections use the "([^"]*)" certificate for encryption')
def then_sip_tls_connections_use_the_group1_certificate_for_encryption(step, certificate):
    certificate_path = "/var/lib/xivo/certificates/%s.pem" % certificate
    current_path = asterisk_helper.get_conf_option('sip.conf', 'general', 'tlscertfile')

    assert_that(current_path, equal_to(certificate_path))


@step(u'Then there are no warnings when reloading sip configuration')
def then_there_are_no_warnings_when_reloading_sip_configuration(step):
    asterisk_helper.send_to_asterisk_cli("sip reload")
    assert not logs.search_str_in_asterisk_log('WARNING')
