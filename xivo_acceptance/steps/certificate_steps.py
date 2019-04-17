# -*- coding: utf-8 -*-
# Copyright 2013-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from lettuce import step

from xivo_acceptance.helpers import asterisk_helper
from xivo_acceptance.lettuce import logs


@step(u'When I create a certificate with the following invalid info:')
def when_i_create_a_certificate_with_the_following_invalid_info(step):
    pass


@step(u'When I create a certificate with following valid info:')
def when_i_create_a_certificate_with_following_valid_info(step):
    pass


@step(u'I create a certificate with following valid info and the server\'s hostname as common name:$')
def i_create_a_certificate_with_following_valid_info_and_the_server_s_hostname_as_common_name(step):
    pass


@step(u'When I enable the following options for the SIP Protocol:')
def when_i_enable_the_following_options_for_the_sip_protocol(step):
    pass


@step(u'Then SIP tls connections use the "([^"]*)" certificate for encryption')
def then_sip_tls_connections_use_the_group1_certificate_for_encryption(step, certificate):
    pass


@step(u'Then there are no warnings when reloading sip configuration')
def then_there_are_no_warnings_when_reloading_sip_configuration(step):
    asterisk_helper.send_to_asterisk_cli(u'module reload res_pjsip.so')
    assert not logs.search_str_in_asterisk_log('WARNING')
