# -*- coding: utf-8 -*-

from lettuce import step
from xivo_lettuce.manager_ws import queue_manager_ws, agent_manager_ws
from xivo_lettuce.common import open_url
from utils import func


@step(u'Given there is no queue "([^"]*)"')
def given_there_is_no_queue_1(step, queue_displayname):
    queue_manager_ws.delete_queue_with_displayname(queue_displayname)


@step(u'Given there is no queue with number "([^"]*)"')
def given_there_is_no_queue_with_number_1(step, queue_number):
    queue_manager_ws.delete_queue_with_number(queue_number)


@step(u'Given there is no queue with name "([^"]+)" or number "([^"]*)"$')
def given_there_is_no_queue_with_name_or_number(step, queue_name, queue_number):
    queue_manager_ws.delete_queue_with_displayname(queue_name)
    queue_manager_ws.delete_queue_with_number(queue_number)


@step(u'Given there is a queue "([^"]+)" with extension "([^"]+)"$')
def given_there_is_a_queue_in_context_with_number(step, name, extension):
    number, context = func.extract_number_and_context_from_extension(extension)
    data = {'name': name,
            'number': number,
            'context': context,
            'maxlen': 0,
            'agents': []}
    queue_manager_ws.add_queue(data)


@step(u'Given there is a queue "([^"]+)" with extension "([^"]+)" with agent "([^"]*)"$')
def given_there_is_a_queue_in_context_with_number_with_agent(step, name, extension, agent_number):
    queue_number, context = func.extract_number_and_context_from_extension(extension)
    agent_id = agent_manager_ws.get_agent_id_with_number(agent_number)
    data = {'name': name,
            'number': queue_number,
            'context': context,
            'maxlen': 0,
            'agents': [agent_id]}
    queue_manager_ws.add_queue(data)


@step(u'Given there is a queue "([^"]+)" saturated with extension "([^"]+)" with agent "([^"]+)"$')
def given_there_is_a_queue_saturated_in_context_with_number_with_agent(step, name, extension, agent_number):
    queue_number, context = func.extract_number_and_context_from_extension(extension)
    agent_id = agent_manager_ws.get_agent_id_with_number(agent_number)
    data = {'name': name,
            'number': queue_number,
            'context': context,
            'maxlen': 1,
            'agents': [agent_id]}
    queue_manager_ws.add_queue(data)


@step(u'When I add a queue')
def when_i_add_a_queue(step):
    open_url('queue', 'add')
