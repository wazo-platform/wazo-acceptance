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
from hamcrest.core import assert_that
from hamcrest.library.collection.isdict_containingentries import has_entries
from lettuce.decorators import step
from lettuce.registry import world

from xivo_acceptance.action.restapi import queue_members_action_restapi
from xivo_acceptance.helpers import queue_helper, agent_helper


@step(u'When I request the queue member information for the queue "([^"]*)" and the agent "([^"]*)"')
def when_i_request_the_queue_member_information_for_the_queue_group1_and_the_agent_group2(step, queue_name, agent_number):
    queue_id = queue_helper.find_queue_id_with_name(queue_name)
    agent_id = agent_helper.find_agent_id_with_number(agent_number)
    world.response = queue_members_action_restapi.get_agent_queue_association(queue_id, agent_id)


@step(u'When I request the queue member information for the queue with id "([^"]*)" and the agent with id "([^"]*)"')
def when_i_request_the_queue_member_information_for_the_queue_with_id_group1_and_the_agent_with_id_group2(step, queue_id, agent_id):
    world.response = queue_members_action_restapi.get_agent_queue_association(queue_id, agent_id)


@step(u'Then I get a queue membership with the following parameters:')
def then_i_get_a_queue_membership_with_the_following_parameters(step):
    queue_member = world.response.data
    assert_that(queue_member, has_entries(step.hashes[0]))
