# -*- coding: utf-8 -*-

import time
from lettuce import step, world
from xivo_lettuce.manager_ws import queue_manager_ws, agent_manager_ws, \
    schedule_manager_ws, user_manager_ws
from utils import func
from xivo_lettuce import common
from xivo_lettuce import form
from xivo_lettuce.manager.queue_manager import type_queue_name_display_name_number_context, \
    remove_queues_with_name_or_number_if_exist, type_queue_ring_strategy
from xivo_lettuce.manager_ws.queue_manager_ws import find_queue_id_with_name


@step(u'Given there is a queue "([^"]+)" with extension "([^"]+)"$')
def given_there_is_a_queue_in_context_with_number(step, name, extension):
    number, context = func.extract_number_and_context_from_extension(extension)
    remove_queues_with_name_or_number_if_exist(name, number)
    data = {'name': name,
            'number': number,
            'context': context}
    queue_manager_ws.add_queue(data)


@step(u'Given there is a queue "([^"]+)" joinempty with extension "([^"]+)"$')
def given_there_is_a_queue_joinempty_with_extension(step, name, extension):
    number, context = func.extract_number_and_context_from_extension(extension)
    remove_queues_with_name_or_number_if_exist(name, number)
    data = {'name': name,
            'number': number,
            'context': context,
            'joinempty': 'unavailable'}
    queue_manager_ws.add_queue(data)


@step(u'Given there is a queue "([^"]+)" closed with extension "([^"]+)"$')
def given_there_is_a_queue_closed_with_extension_with_agent(step, name, extension):
    number, context = func.extract_number_and_context_from_extension(extension)
    remove_queues_with_name_or_number_if_exist(name, number)
    opened = {'hours': '00:00-00:01',
              'weekdays': '1-1',
              'monthdays': '1-1',
              'months': '1-1'}
    schedule_manager_ws.delete_schedules_with_name('always_closed')
    schedule_manager_ws.add_schedule('always_closed', opened)
    schedule_id = schedule_manager_ws.find_schedule_id_with_name('always_closed')

    data = {'name': name,
            'number': number,
            'context': context,
            'schedule_id': schedule_id}
    queue_manager_ws.add_queue(data)


@step(u'Given there is a queue "([^"]+)" leaveempty with extension "([^"]+)" with agent "([^"]+)"$')
def given_there_is_a_queue_leaveempty_with_extension_with_agent(step, name, extension, agent_number):
    number, context = func.extract_number_and_context_from_extension(extension)
    remove_queues_with_name_or_number_if_exist(name, number)
    agent_id = agent_manager_ws.find_agent_id_with_number(agent_number)
    data = {'name': name,
            'number': number,
            'context': context,
            'leavewhenempty': 'unavailable,paused',
            'agents': [agent_id]}
    queue_manager_ws.add_queue(data)


@step(u'^Given there is a queue "([^"]*)" with extension "([^"]*)" with user "([^"]*)"')
def given_there_is_a_queue_group1_with_extension_group2_with_user_group3(step, name, extension, user_number):
    number, context = func.extract_number_and_context_from_extension(extension)
    remove_queues_with_name_or_number_if_exist(name, number)
    user_ids = user_manager_ws.search_user_ids_with_number(user_number, context)
    data = {
        'name': name,
        'number': number,
        'context': context,
        'users': user_ids,
    }
    queue_manager_ws.add_queue(data)


@step(u'Given there is a queue "([^"]+)" with ringing time of "([0-9]+)s" with extension "([^"]+)" with agent "([^"]+)"')
def given_there_is_a_queue_with_ringing_time_with_extension_with_agent(step, name, ringing_time, extension, agent_number):
    number, context = func.extract_number_and_context_from_extension(extension)
    remove_queues_with_name_or_number_if_exist(name, number)
    agent_id = agent_manager_ws.find_agent_id_with_number(agent_number)
    data = {'name': name,
            'number': number,
            'context': context,
            'ringing_time': ringing_time,
            'agents': [agent_id]}
    queue_manager_ws.add_queue(data)


@step(u'Given there is a queue "([^"]+)" with extension "([^"]+)" with agent "([^"]*)"$')
def given_there_is_a_queue_in_context_with_extension_with_agent(step, name, extension, agent_number):
    number, context = func.extract_number_and_context_from_extension(extension)
    remove_queues_with_name_or_number_if_exist(name, number)
    agent_id = agent_manager_ws.find_agent_id_with_number(agent_number)
    data = {'name': name,
            'number': number,
            'context': context,
            'agents': [agent_id]}
    queue_manager_ws.add_queue(data)


@step(u'Given there is a queue "([^"]+)" saturated with extension "([^"]+)" with agent "([^"]+)"$')
def given_there_is_a_queue_saturated_in_context_with_extension_with_agent(step, name, extension, agent_number):
    number, context = func.extract_number_and_context_from_extension(extension)
    remove_queues_with_name_or_number_if_exist(name, number)
    agent_id = agent_manager_ws.find_agent_id_with_number(agent_number)
    data = {'name': name,
            'number': number,
            'context': context,
            'maxlen': 1,
            'agents': [agent_id]}
    queue_manager_ws.add_queue(data)


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
        agent_id = agent_manager_ws.add_or_replace_agent(agent_data)
        agent_ids.append(agent_id)

    queue_data = {
        'name': queue_name,
        'number': queue_number,
        'context': queue_context,
        'agents': agent_ids,
    }

    queue_manager_ws.add_or_replace_queue(queue_data)


@step(u'When I add the queue "([^"]*)" with display name "([^"]*)" with extension "([^"]*)" in "([^"]*)"$')
def when_i_add_the_queue_1_with_display_name_2_with_extension_3_in_4(step, name, display_name, extension, context):
    remove_queues_with_name_or_number_if_exist(name, extension)
    common.open_url('queue', 'add')
    type_queue_name_display_name_number_context(name, display_name, extension, context)
    form.submit.submit_form()


@step(u'When I add the queue "([^"]*)" with display name "([^"]*)" with extension "([^"]*)" in "([^"]*)" with errors$')
def when_i_add_the_queue_1_with_display_name_2_with_extension_3_in_4_with_errors(step, name, display_name, extension, context):
    remove_queues_with_name_or_number_if_exist(name, extension)
    common.open_url('queue', 'add')
    type_queue_name_display_name_number_context(name, display_name, extension, context)
    form.submit.submit_form_with_errors()


@step(u'When I add the queue "([^"]*)" with extension "([^"]*)" with ring strategy at "([^"]*)"$')
def when_i_add_the_queue_group1_with_extension_group2_with_ring_strategy_at_group3(step, queue_name, extension, ring_strategy):
    number, context = func.extract_number_and_context_from_extension(extension)
    remove_queues_with_name_or_number_if_exist(queue_name, number)
    common.open_url('queue', 'add')
    type_queue_name_display_name_number_context(queue_name, queue_name, number, context)
    type_queue_ring_strategy(ring_strategy)
    form.submit.submit_form()


@step(u'When I edit the queue "([^"]*)"$')
def when_i_edit_the_queue_group1(step, queue_name):
    queue_id = find_queue_id_with_name(queue_name)
    common.open_url('queue', 'edit', {'id': queue_id})
    form.submit.submit_form()


@step(u'When I edit the queue "([^"]*)" and set ring strategy at "([^"]*)"$')
def when_i_edit_the_queue_group1_and_set_ring_strategy_at_group2(step, queue_name, ring_strategy):
    queue_id = find_queue_id_with_name(queue_name)
    common.open_url('queue', 'edit', {'id': queue_id})
    type_queue_ring_strategy(ring_strategy)
    form.submit.submit_form()


@step(u'When I add agent "([^"]*)" to "([^"]*)"')
def when_i_add_agent_1_to_2(step, agent_number, queue_name):
    queue = queue_manager_ws.get_queue_with_name(queue_name)
    agent_id = agent_manager_ws.find_agent_id_with_number(agent_number)
    queue.agents.append(agent_id)
    world.ws.queues.edit(queue)
    time.sleep(5)


@step(u'When I remove agent "([^"]*)" from "([^"]*)"')
def when_i_remove_agent_1_from_2(step, agent_number, queue_name):
    queue = queue_manager_ws.get_queue_with_name(queue_name)
    agent_id = agent_manager_ws.find_agent_id_with_number(agent_number)
    queue.agents.remove(agent_id)
    world.ws.queues.edit(queue)
    time.sleep(10)


@step(u'When I edit the queue "([^"]*)" and set ring strategy at "([^"]*)" with errors$')
def when_i_edit_the_queue_group1_and_set_ring_strategy_at_group2_with_errors(step, queue_name, ring_strategy):
    queue_id = find_queue_id_with_name(queue_name)
    common.open_url('queue', 'edit', {'id': queue_id})
    type_queue_ring_strategy(ring_strategy)
    form.submit.submit_form_with_errors()
