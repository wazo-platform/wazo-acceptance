# -*- coding: utf-8 -*-

from lettuce.decorators import step
from xivo_lettuce.manager import queue_manager, agent_manager


@step(u'Given there is a queue "([^"]+)" in context "([^"]+)" with number "([^"]+)" that is statured$')
def given_there_is_a_queue_in_context_with_number_that_is_statured(step, name, context, number):
    agent_id = agent_manager.insert_agent_if_not_exist('test', 'test', '7878', '')
    data = {'name': name,
            'number': number,
            'context': context,
            'maxlen': 1,
            'agents': agent_id}
    queue_manager.insert_queue(data)
