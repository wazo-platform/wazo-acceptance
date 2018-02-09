# -*- coding: utf-8 -*-
# Copyright (C) 2013-2014 Avencall
# SPDX-License-Identifier: GPL-3.0+

from lettuce import step
from hamcrest import *

from xivo_acceptance.helpers import queue_helper, cti_helper


@step(u'Then the Queue members xlet is empty')
def then_the_queue_members_xlet_is_empty(step):
    res = cti_helper.get_queue_members_infos()
    assert_that(res['return_value']['row_count'], equal_to(0))


@step(u'Then the Queue members xlet for queue "([^"]*)" is empty')
def then_the_queue_members_xlet_for_queue_1_is_empty(step, queue_name):
    queue_id = queue_helper.find_queue_id_with_name(queue_name)
    cti_helper.set_queue_for_queue_members(queue_id)
    res = cti_helper.get_queue_members_infos()
    assert_that(res['return_value']['row_count'], equal_to(0))


@step(u'Then the Queue members xlet for queue "([^"]*)" should display agents:')
def then_the_queue_members_xlet_for_queue_1_should_display_agents(step, queue_name):
    queue_id = queue_helper.find_queue_id_with_name(queue_name)
    cti_helper.set_queue_for_queue_members(queue_id)
    res = cti_helper.get_queue_members_infos()
    assert_that(res['return_value']['row_count'], greater_than(0))
