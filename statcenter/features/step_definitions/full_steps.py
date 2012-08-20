# -*- coding: utf-8 -*-

from lettuce.decorators import step
from xivo_lettuce.manager import queue_manager, agent_manager


@step(u'Given there is a queue "([^"]+)" statured in context "([^"]+)" with number "([^"]+)" with agent "([^"]+)"$')
def given_there_is_a_queue_statured_in_context_with_number_with_agent(step, name, context, queue_number, agent_number):
    agent_id = agent_manager.find_agent_id_from_number(agent_number)
    data = {'name': name,
            'number': queue_number,
            'context': context,
            'maxlen': 1,
            'agents': agent_id}
    queue_manager.insert_queue(data)
