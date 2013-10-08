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

from lettuce import step
from hamcrest import *

from xivo_acceptance.helpers import queue_helper
from xivo_lettuce.manager import cti_client_manager


@step(u'Then the Queue members xlet is empty')
def then_the_queue_members_xlet_is_empty(step):
    res = cti_client_manager.get_queue_members_infos()
    assert_that(res['return_value']['row_count'], equal_to(0))


@step(u'Then the Queue members xlet for queue "([^"]*)" is empty')
def then_the_queue_members_xlet_for_queue_1_is_empty(step, queue_name):
    queue_id = queue_helper.find_queue_id_with_name(queue_name)
    cti_client_manager.set_queue_for_queue_members(queue_id)
    res = cti_client_manager.get_queue_members_infos()
    assert_that(res['return_value']['row_count'], equal_to(0))


@step(u'Then the Queue members xlet for queue "([^"]*)" should display agents:')
def then_the_queue_members_xlet_for_queue_1_should_display_agents(step, queue_name):
    queue_id = queue_helper.find_queue_id_with_name(queue_name)
    cti_client_manager.set_queue_for_queue_members(queue_id)
    res = cti_client_manager.get_queue_members_infos()
    assert_that(res['return_value']['row_count'], greater_than(0))
