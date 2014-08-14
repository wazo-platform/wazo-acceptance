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

from hamcrest import assert_that, equal_to
from lettuce import step
from xivo_acceptance.helpers import agent_helper
from xivo_lettuce import agi, logs


@step(u'When (\d+) simultaneous AGI requests are done to get the status of agent (\d+)')
def when_10_simultaneous_agi_requests_are_done_to_get_the_status_of_agent_1001(step, nb_request, agent_number):
    nb_request = int(nb_request)

    agent_id = agent_helper.find_agent_id_with_number(agent_number)
    agi.do_simultaneous_requests(nb_request, 'agent_get_status', [agent_id])


@step(u'Then there\'s no error in xivo-agid log file')
def then_there_s_no_error_in_xivo_agid_log_file(step):
    errors_found = logs.search_str_in_xivo_agid_log("ERROR")
    assert_that(errors_found, equal_to(False), 'errors were found in xivo-agid logs')
