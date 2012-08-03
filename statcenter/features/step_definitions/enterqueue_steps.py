# -*- coding: utf-8 -*-

from lettuce.decorators import step
from xivo_lettuce.manager import queuelog_manager


@step(u'Given there is ([0-9]+) calls enter in queue "([^"]*)" with number "([^"]*)"$')
def given_there_is_a_n_calls_statured_in_queue(step, count, queuename, number):
    queuelog_manager.execute_call_event_enterqueue(count, queuename, number)
