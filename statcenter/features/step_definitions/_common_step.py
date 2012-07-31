# -*- coding: UTF-8 -*-

import time
from lettuce.decorators import step
from xivo_lettuce.manager import queuelog_manager


@step(u'Given there is no "([^"]*)" entry in queue "([^"]*)')
def given_there_is_no_event_entry_in_queue_log_table_in_queue_queue(step, event, queue_name):
    queuelog_manager.delete_event_by_queue(event, queue_name)


@step(u'Then i should see ([0-9]+) "([^"]*)" calls in queue "([^"]*)" in the queue log')
def then_i_should_see_nb_group1_calls_in_queue_group2_in_the_queue_log(step, expected_count, event, queue_name):
    count = queuelog_manager.get_event_count_queue(event, queue_name)

    assert(count == int(expected_count))


@step(u'Given I wait ([0-9]+) seconds for the dialplan to be reloaded')
def given_i_wait_n_seconds_for_the_dialplan_to_be_reloaded(step, count):
    time.sleep(int(count))
