# -*- coding: utf-8 -*-

from lettuce.decorators import step
from xivo_lettuce.manager import queue_manager, queuelog_manager, agent_manager
from xivo_lettuce.manager.context_manager import add_contextnumbers_queue


@step(u'Given there is a queue "([^"]+)" in context "([^"]+)" with number "([^"]+)" that is statured$')
def given_there_is_a_queue_in_context_with_number_that_is_statured(step, name, context, number):
    add_contextnumbers_queue(context, number, number)
    agent_manager.insert_agent('test', 'test', '7878', '')
    agent_id = agent_manager.find_agent_id_from_number('7878')
    data = {'name': name,
            'number': number,
            'context': context,
            'maxlen': 1,
            'agents': agent_id}
    queue_manager.insert_queue(data)


@step(u'Given there is ([0-9]+) calls satured in queue "([^"]+)" with number "([^"]+)"$')
def given_there_is_a_n_calls_statured_in_queue(step, count, queuename, number):
    queuelog_manager.execute_call_event_full(count, queuename, number)
