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

import time

from lettuce import step, world

from xivo_acceptance.helpers import user_helper, agent_helper, queue_helper
from xivo_lettuce.manager_ws import schedule_manager_ws, user_manager_ws
from xivo_lettuce.manager import queue_manager
from xivo_lettuce import common
from xivo_lettuce import form


@step(u'^Given there are queues with infos:$')
def given_there_are_queues_with_infos(step):
    for info in step.hashes:
        queue_data = dict(info)

        if queue_data.get('users_number'):
            queue_data['users'] = convert_user_numbers(queue_data.pop('users_number'), queue_data['context'])

        if queue_data.get('agents_number'):
            queue_data['agents'] = convert_agent_numbers(queue_data.pop('agents_number'))

        if queue_data.get('schedule_name'):
            queue_data['schedule_id'] = convert_schedule_name(queue_data.pop('schedule_name'))

        queue_helper.add_or_replace_queue(queue_data)


def convert_user_numbers(user_numbers, context):
    users = []
    user_number_list = user_numbers.split(',')
    for user_number in user_number_list:
        user = user_helper.get_by_exten_context(user_number, context)
        if user:
            users.extend([user.id])
    return users


def convert_agent_numbers(agent_numbers):
    agent_ids = []
    agent_number_list = agent_numbers.split(',')
    for agent_number in agent_number_list:
        agent_id = agent_helper.find_agent_id_with_number(agent_number.strip())
        agent_ids.append(agent_id)
    return agent_ids


def convert_schedule_name(schedule_name):
    schedule_id = schedule_manager_ws.find_schedule_id_with_name(schedule_name)
    return schedule_id


@step(u'Given there is a queue "([^"]*)" with number "([^"]*)" in "([^"]*)" and unlogged members:')
def given_there_is_a_queue_queue_name_with_number_number_and_unlogged_members(step, queue_name, queue_number, queue_context):
    agent_ids = []
    for agent_data in step.hashes:
        user_data = {
            'firstname': agent_data['firstname'],
            'lastname': agent_data['lastname'],
            'line_number': agent_data['number'],
            'line_context': agent_data['context'],
        }
        user_id = user_manager_ws.add_or_replace_user(user_data)
        agent_data['users'] = [user_id]
        agent_id = agent_helper.add_or_replace_agent(agent_data)
        agent_ids.append(agent_id)

    queue_data = {
        'name': queue_name,
        'number': queue_number,
        'context': queue_context,
        'agents': agent_ids,
    }

    queue_helper.add_or_replace_queue(queue_data)


@step(u'When I create the following queues:')
def when_i_create_the_following_queues(step):
    for queue in step.hashes:
        queue_manager.add_or_replace_queue(queue)
        form.submit.submit_form()


@step(u'When I create the following invalid queues:')
def when_i_create_the_following_invalid_queues(step):
    for queue in step.hashes:
        queue_manager.add_or_replace_queue(queue)
        form.submit.submit_form_with_errors()


@step(u'When I edit the queue "([^"]*)"$')
def when_i_edit_the_queue_group1(step, queue_name):
    queue_id = queue_helper.find_queue_id_with_name(queue_name)
    common.open_url('queue', 'edit', {'id': queue_id})
    form.submit.submit_form()


@step(u'When I edit the queue "([^"]*)" and set ring strategy at "([^"]*)"$')
def when_i_edit_the_queue_group1_and_set_ring_strategy_at_group2(step, queue_name, ring_strategy):
    queue_id = queue_helper.find_queue_id_with_name(queue_name)
    common.open_url('queue', 'edit', {'id': queue_id})
    queue_manager.type_queue_ring_strategy(ring_strategy)
    form.submit.submit_form()


@step(u'When I edit the queue "([^"]*)" and set ring strategy at "([^"]*)" with errors$')
def when_i_edit_the_queue_group1_and_set_ring_strategy_at_group2_with_errors(step, queue_name, ring_strategy):
    queue_id = queue_helper.find_queue_id_with_name(queue_name)
    common.open_url('queue', 'edit', {'id': queue_id})
    queue_manager.type_queue_ring_strategy(ring_strategy)
    form.submit.submit_form_with_errors()


@step(u'When I add agent "([^"]*)" to "([^"]*)"')
def when_i_add_agent_1_to_2(step, agent_number, queue_name):
    queue = queue_helper.get_queue_with_name(queue_name)
    agent_id = agent_helper.find_agent_id_with_number(agent_number)
    queue.agents.append(agent_id)
    world.ws.queues.edit(queue)
    time.sleep(5)


@step(u'When I add the agent with extension "([^"]*)" to the queue "([^"]*)"')
def when_i_add_the_agent_with_extension_group1_to_the_queue_group2(step, extension, queue_name):
    queue_id = queue_helper.find_queue_id_with_name(queue_name)
    common.open_url('queue', 'edit', {'id': queue_id})
    queue_manager.add_agents_to_queue([extension])
    form.submit.submit_form()


@step(u'When I remove agent "([^"]*)" from "([^"]*)"')
def when_i_remove_agent_1_from_2(step, agent_number, queue_name):
    queue = queue_helper.get_queue_with_name(queue_name)
    agent_id = agent_helper.find_agent_id_with_number(agent_number)
    queue.agents.remove(agent_id)
    world.ws.queues.edit(queue)
    time.sleep(10)


@step(u'When I remove the agent with extension "([^"]*)" from the queue "([^"]*)"')
def when_i_remove_the_agent_with_extension_group1_from_the_queue_group2(step, extension, queue_name):
    queue_id = queue_helper.find_queue_id_with_name(queue_name)
    common.open_url('queue', 'edit', {'id': queue_id})
    queue_manager.remove_agents_from_queue([extension])
    form.submit.submit_form()


@step(u'When I delete the queue with number "([^"]*)"')
def when_i_delete_the_queue_with_number_group1(step, queue_number):
    common.open_url('queue', 'list')
    common.remove_line(queue_number)
    time.sleep(3)


@step(u'Then the agent "([^"]*)" is a member of the queue "([^"]*)" in asterisk')
def then_the_agent_group1_is_a_member_of_the_queue_group2_in_asterisk(step, agent_number, queue_name):
    agent_numbers = queue_manager.agent_numbers_from_asterisk(queue_name)
    assert int(agent_number) in agent_numbers


@step(u'Then the agent "([^"]*)" is not a member of the queue "([^"]*)" in asterisk')
def then_the_agent_group1_is_not_a_member_of_the_queue_group2_in_asterisk(step, agent_number, queue_name):
    agent_numbers = queue_manager.agent_numbers_from_asterisk(queue_name)
    assert int(agent_number) not in agent_numbers


@step(u'Then the queue "([^"]*)" does not exist in asterisk')
def then_the_queue_group1_does_not_exist_in_asterisk(step, queue_name):
    assert not queue_manager.does_queue_exist_in_asterisk(queue_name)
