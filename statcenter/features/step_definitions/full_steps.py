# -*- coding: utf-8 -*-

from lettuce.decorators import step
from xivo_lettuce.manager import queue_manager, queuelog_manager, agent_manager
from xivo_lettuce.manager.context_manager import add_context_queue, \
    delete_context


@step(u'Given there is a queue "([^"]*)" with number "([^"]*)" that is statured$')
def given_there_is_a_queue_that_is_statured(step, name, number):
    context_name = 'ctx_%s' % name.lower()
    delete_context(context_name)
    add_context_queue(context_name, context_name, number, number)
    agent_manager.insert_agent('test', 'test', '7878', '')
    agent_id = agent_manager.find_agent_id_from_number('7878')
    data = {'name': name,
            'number': number,
            'context': context_name,
            'maxlen': 1,
            'agents': agent_id}
    queue_manager.insert_queue(data)


@step(u'Given there is ([0-9]+) calls satured in queue "([^"]*)" with number "([^"]*)"$')
def given_there_is_a_n_calls_statured_in_queue(step, count, queuename, number):
    queuelog_manager.execute_call_event_full(count, queuename, number)
