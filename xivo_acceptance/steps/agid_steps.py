# -*- coding: utf-8 -*-
# Copyright 2013-2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from hamcrest import assert_that, equal_to
from lettuce import step
from xivo_acceptance.helpers import agent_helper
from xivo_acceptance.lettuce import agi, logs


@step(u'When (\d+) simultaneous AGI requests are done to get the status of agent (\d+)')
def when_10_simultaneous_agi_requests_are_done_to_get_the_status_of_agent_1001(step, nb_request, agent_number):
    nb_request = int(nb_request)

    agent_id = agent_helper.find_agent_by(number=agent_number)['id']
    agi.do_simultaneous_requests(nb_request, 'agent_get_status', [agent_id])


@step(u'Then there\'s no error in xivo-agid log file')
def then_there_s_no_error_in_xivo_agid_log_file(step):
    errors_found = logs.search_str_in_xivo_agid_log("ERROR")
    assert_that(errors_found, equal_to(False), 'errors were found in xivo-agid logs')
