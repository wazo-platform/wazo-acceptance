# -*- coding: utf-8 -*-
# Copyright 2013-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later


from hamcrest import assert_that, equal_to
from lettuce import step

from xivo_acceptance.helpers import cti_helper
from xivo_acceptance.lettuce import common
from xivo_acceptance.lettuce import xivoclient


@step(u'I log in the XiVO Client as "([^"]*)", pass "([^"]*)"$')
def i_log_in_the_xivo_client_as_1_pass_2(step, login, password):
    conf_dict = {
        'main_server_address': common.get_host_address(),
        'login': login,
        'password': password,
        'agent_option': 'no',
    }
    cti_helper.configure_client(conf_dict)
    result = cti_helper.log_in_the_xivo_client()
    assert_that(result['test_result'], equal_to('passed'),
                'could not log in the CTI client as %s pass %s' % (login, password))


@step(u'I start the XiVO Client$')
def i_start_the_xivo_client(step):
    xivoclient.start_xivoclient()
