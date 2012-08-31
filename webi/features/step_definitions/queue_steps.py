# -*- coding: utf-8 -*-

from lettuce import step
from xivo_lettuce.manager_ws import queue_manager_ws, agent_manager_ws, \
    context_manager_ws, schedule_manager_ws
from utils import func
from xivo_lettuce import common, form


@step(u'Given there is no queue "([^"]*)"')
def given_there_is_no_queue_1(step, queue_name):
    queue_manager_ws.delete_queue_with_name_if_exists(queue_name)


@step(u'Given there is no queue with number "([^"]*)"')
def given_there_is_no_queue_with_number_1(step, queue_number):
    queue_manager_ws.delete_queue_with_number_if_exists(queue_number)


@step(u'Given there is a queue "([^"]+)" with extension "([^"]+)"$')
def given_there_is_a_queue_in_context_with_number(step, name, extension):
    number, context = func.extract_number_and_context_from_extension(extension)
    _remove_queues_with_name_or_number_if_exist(name, number)
    data = {'name': name,
            'number': number,
            'context': context}
    queue_manager_ws.add_queue(data)


@step(u'Given there is a queue "([^"]+)" joinempty with extension "([^"]+)"$')
def given_there_is_a_queue_joinempty_with_extension(step, name, extension):
    number, context = func.extract_number_and_context_from_extension(extension)
    _remove_queues_with_name_or_number_if_exist(name, number)
    data = {'name': name,
            'number': number,
            'context': context,
            'joinempty': 'unavailable'}
    queue_manager_ws.add_queue(data)


@step(u'Given there is a queue "([^"]+)" diverted with extension "([^"]+)" with agent "([^"]+)"$')
def given_there_is_a_queue_diverted_with_extension_with_agent(step, name, extension, agent_number):
    number, context = func.extract_number_and_context_from_extension(extension)
    _remove_queues_with_name_or_number_if_exist(name, number)
    agent_id = agent_manager_ws.get_agent_id_with_number(agent_number)
    data = {'name': name,
            'number': number,
            'context': context,
            'agents': [agent_id],
            'waittime': 5,
            'waitratio': 100}
    queue_manager_ws.add_queue(data)


@step(u'Given there is a queue "([^"]+)" closed with extension "([^"]+)" with agent "([^"]+)"$')
def given_there_is_a_queue_closed_with_extension_with_agent(step, name, extension, agent_number):
    number, context = func.extract_number_and_context_from_extension(extension)
    _remove_queues_with_name_or_number_if_exist(name, number)
    opened = {'hours': '00:00-00:01',
               'weekdays': '1-1',
               'monthdays': '1-1',
               'months': '1-1'
               }
    schedule_manager_ws.delete_schedule_with_name('always_closed')
    schedule_manager_ws.add_schedule('always_closed', opened)
    schedule_id = schedule_manager_ws.get_schedule_id_with_name('always_closed')

    data = {'name': name,
            'number': number,
            'context': context,
            'schedule_id': schedule_id}
    queue_manager_ws.add_queue(data)


@step(u'Given there is a queue "([^"]+)" leaveempty with extension "([^"]+)" with agent "([^"]+)"$')
def given_there_is_a_queue_leaveempty_with_extension_with_agent(step, name, extension, agent_number):
    number, context = func.extract_number_and_context_from_extension(extension)
    _remove_queues_with_name_or_number_if_exist(name, number)
    agent_id = agent_manager_ws.get_agent_id_with_number(agent_number)
    data = {'name': name,
            'number': number,
            'context': context,
            'leavewhenempty': 'unavailable, pause',
            'agents': [agent_id]}
    queue_manager_ws.add_queue(data)


@step(u'Given there is a queue "([^"]+)" with extension "([^"]+)" with agent "([^"]*)"$')
def given_there_is_a_queue_in_context_with_extension_with_agent(step, name, extension, agent_number):
    number, context = func.extract_number_and_context_from_extension(extension)
    _remove_queues_with_name_or_number_if_exist(name, number)
    agent_id = agent_manager_ws.get_agent_id_with_number(agent_number)
    data = {'name': name,
            'number': number,
            'context': context,
            'agents': [agent_id]}
    queue_manager_ws.add_queue(data)


@step(u'Given there is a queue "([^"]+)" saturated with extension "([^"]+)" with agent "([^"]+)"$')
def given_there_is_a_queue_saturated_in_context_with_extension_with_agent(step, name, extension, agent_number):
    number, context = func.extract_number_and_context_from_extension(extension)
    _remove_queues_with_name_or_number_if_exist(name, number)
    agent_id = agent_manager_ws.get_agent_id_with_number(agent_number)
    data = {'name': name,
            'number': number,
            'context': context,
            'maxlen': 1,
            'agents': [agent_id]}
    queue_manager_ws.add_queue(data)


@step(u'When I add the queue "([^"]*)" with display name "([^"]*)" with extension "([^"]*)" in "([^"]*)"$')
def when_i_add_the_queue_1_with_display_name_2_with_extension_3_in_4(step, name, display_name, extension, context):
    _remove_queues_with_name_or_number_if_exist(name, extension)
    common.open_url('queue', 'add')
    _type_queue_name_display_name_number_context(name, display_name, extension, context)
    common.submit_form()


@step(u'When I add the queue "([^"]*)" with display name "([^"]*)" with extension "([^"]*)" in "([^"]*)" with errors$')
def when_i_add_the_queue_1_with_display_name_2_with_extension_3_in_4_with_errors(step, name, display_name, extension, context):
    _remove_queues_with_name_or_number_if_exist(name, extension)
    common.open_url('queue', 'add')
    _type_queue_name_display_name_number_context(name, display_name, extension, context)
    form.submit_form_with_errors()


def _remove_queues_with_name_or_number_if_exist(queue_name, queue_number):
    queue_manager_ws.delete_queue_with_name_if_exists(queue_name)
    queue_manager_ws.delete_queue_with_number_if_exists(queue_number)


def _type_queue_name_display_name_number_context(name, display_name, extension, context):
    form.set_text_field('Name', name)
    form.set_text_field('Display name', display_name)
    form.set_text_field('Number', extension)
    context = context_manager_ws.get_context_with_name(context)
    context_field_value = '%s (%s)' % (context.display_name, context.name)
    form.set_select_field('Context', context_field_value)
