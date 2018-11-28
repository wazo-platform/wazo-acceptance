# -*- coding: utf-8 -*-
# Copyright 2013-2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

import time
from hamcrest import assert_that, contains
from lettuce import step, world

from xivo_acceptance.action.webi import queue as queue_action_webi
from xivo_acceptance.helpers import (
    agent_helper,
    asterisk_helper,
    queue_helper,
    schedule_helper,
    user_helper,
)
from xivo_acceptance.lettuce import common, form


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
        user = user_helper.find_by_exten_context(user_number, context)
        if user:
            users.append(user['id'])
    return users


def convert_agent_numbers(agent_numbers):
    agent_ids = []
    agent_number_list = agent_numbers.split(',')
    for agent_number in agent_number_list:
        agent_id = agent_helper.find_agent_by(number=agent_number.strip())['id']
        agent_ids.append(agent_id)
    return agent_ids


def convert_schedule_name(schedule_name):
    schedule_id = schedule_helper.find_schedule_id_with_name(schedule_name)
    return schedule_id


@step(u'When I create the following queues:')
def when_i_create_the_following_queues(step):
    for queue in step.hashes:
        queue_action_webi.add_or_replace_queue(queue)
        form.submit.submit_form()


@step(u'When I create the following invalid queues:')
def when_i_create_the_following_invalid_queues(step):
    for queue in step.hashes:
        queue_action_webi.add_or_replace_queue(queue)
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
    queue_action_webi.type_queue_ring_strategy(ring_strategy)
    form.submit.submit_form()


@step(u'When I edit the queue "([^"]*)" and set ring strategy at "([^"]*)" with errors$')
def when_i_edit_the_queue_group1_and_set_ring_strategy_at_group2_with_errors(step, queue_name, ring_strategy):
    queue_id = queue_helper.find_queue_id_with_name(queue_name)
    common.open_url('queue', 'edit', {'id': queue_id})
    queue_action_webi.type_queue_ring_strategy(ring_strategy)
    form.submit.submit_form_with_errors()


@step(u'When I add agent "([^"]*)" to "([^"]*)"')
def when_i_add_agent_1_to_2(step, agent_number, queue_name):
    queue = queue_helper.get_queue_with_name(queue_name)
    agent_id = agent_helper.find_agent_by(number=agent_number)['id']
    queue.agents.append(agent_id)
    world.ws.queues.edit(queue)
    time.sleep(5)


@step(u'When I add the agent with extension "([^"]*)" to the queue "([^"]*)"')
def when_i_add_the_agent_with_extension_group1_to_the_queue_group2(step, extension, queue_name):
    queue_id = queue_helper.find_queue_id_with_name(queue_name)
    common.open_url('queue', 'edit', {'id': queue_id})
    queue_action_webi.add_agents_to_queue([extension])
    form.submit.submit_form()


@step(u'When I remove agent "([^"]*)" from "([^"]*)"')
def when_i_remove_agent_1_from_2(step, agent_number, queue_name):
    queue = queue_helper.get_queue_with_name(queue_name)
    agent_id = agent_helper.find_agent_by(number=agent_number)['id']
    queue.agents.remove(agent_id)
    world.ws.queues.edit(queue)
    time.sleep(10)


@step(u'When I remove the agent with extension "([^"]*)" from the queue "([^"]*)"')
def when_i_remove_the_agent_with_extension_group1_from_the_queue_group2(step, extension, queue_name):
    queue_id = queue_helper.find_queue_id_with_name(queue_name)
    common.open_url('queue', 'edit', {'id': queue_id})
    queue_action_webi.remove_agents_from_queue([extension])
    form.submit.submit_form()


@step(u'When I delete the queue with extension "([^"]*)@([^"]*)"')
def when_i_delete_the_queue_with_number_group1(step, exten, context):
    queues = queues_with_exten(exten, context)
    assert queues, "No queue with extension {exten}@{context}".format(exten=exten, context=context)
    queue_id = queues[0].id
    common.open_url('queue', 'delete', {'id': queue_id})
    common.wait_until(queue_is_no_longer_in_list, exten, context, tries=5)


def queue_is_no_longer_in_list(exten, context):
    queues = queues_with_exten(exten, context)
    return len(queues) == 0


def queues_with_exten(exten, context):
    return [queue for queue in world.ws.queues.search(exten) if queue.number == exten and queue.context == context]


@step(u'Then the agent "([^"]*)" is a member of the queue "([^"]*)" in asterisk')
def then_the_agent_group1_is_a_member_of_the_queue_group2_in_asterisk(step, agent_number, queue_name):
    agent_numbers = queue_helper.agent_numbers_from_asterisk(queue_name)
    assert int(agent_number) in agent_numbers


@step(u'Then the agent "([^"]*)" is not a member of the queue "([^"]*)" in asterisk')
def then_the_agent_group1_is_not_a_member_of_the_queue_group2_in_asterisk(step, agent_number, queue_name):
    agent_numbers = queue_helper.agent_numbers_from_asterisk(queue_name)
    assert int(agent_number) not in agent_numbers


@step(u'Then the queue "([^"]*)" does not exist in asterisk')
def then_the_queue_group1_does_not_exist_in_asterisk(step, queue_name):
    assert not queue_helper.does_queue_exist_in_asterisk(queue_name)


@step(u'Then I see the queue "([^"]*)" exists$')
def then_i_see_the_element_exists(step, name):
    common.open_url('queue')
    line = common.find_line(name)
    assert line is not None, 'queue: %s does not exist' % name


@step(u'Then I see the queue "([^"]*)" not exists$')
def then_i_see_the_element_not_exists(step, name):
    common.open_url('queue')
    line = common.find_line(name)
    assert line is None, 'queue: %s exist' % name


@step(u'When I edit the queue "([^"]*)" and set exit context at "([^"]*)"')
def when_i_edit_the_queue_group1_and_set_exit_context_at_group2(step, queue_name, context_name):
    queue_id = queue_helper.find_queue_id_with_name(queue_name)
    common.open_url('queue', 'edit', {'id': queue_id})
    common.go_to_tab('Advanced')
    queue_action_webi.type_queue_exit_context(context_name)
    form.submit.submit_form()


@step(u'Then the exit context is "([^"]*)" for queue "([^"]*)" in asterisk')
def then_the_exit_context_is_group1_for_queue_group2_in_asterisk(step, context_name, queue_name):
    options = asterisk_helper.get_conf_options('queues.conf', queue_name, ['context'])
    expected_option = [(u'context', context_name)]
    assert_that(options, contains(*expected_option))
