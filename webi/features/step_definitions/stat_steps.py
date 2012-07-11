# -*- coding: utf-8 -*-

from lettuce.decorators import step
from xivo_lettuce.manager import queue_manager, queuelog_manager, agent_manager
from xivo_lettuce.manager.context_manager import check_context_number_in_interval
import subprocess
import time
import os


_ACCEPTANCE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
_LOAD_TESTER_SCRIPT = os.path.join(_ACCEPTANCE_ROOT, 'load-tester/load-tester')
_CONFIG_DIR = os.path.join(_ACCEPTANCE_ROOT, 'load-tester-conf-custom')
_CONFIG_FILE = os.path.join(_CONFIG_DIR, 'call_exten.py')
_SC_CALL_THEN_HANGUP = os.path.join(_ACCEPTANCE_ROOT, 'load-tester/scenarios/call-then-hangup')
_SC_CALL_THEN_WAIT = os.path.join(_ACCEPTANCE_ROOT, 'load-tester/scenarios/call-then-wait')


@step(u'Given there is a queue "([^"]*)" with number "([^"]*)" that is statured$')
def given_there_is_a_queue_that_is_statured(step, name, number):
    agent_manager.insert_agent('test', 'test', '7878', '')
    agent_id = agent_manager.find_agent_id_from_number('7878')
    check_context_number_in_interval('default', 'queue', number)
    data = {'name': name,
            'number': number,
            'maxlen': 1,
            'agents': agent_id}
    queue_manager.insert_queue(data)


@step(u'Given there is ([0-9]+) calls satured in queue "([^"]*)" with number "([^"]*)"$')
def given_there_is_a_3_calls_statured_in_queue(step, count, name, number):
    _cmd_base = [_LOAD_TESTER_SCRIPT, 'start', '-c', _CONFIG_FILE]
    cmd_1 = _cmd_base + [_SC_CALL_THEN_HANGUP]
    cmd_2 = _cmd_base + [_SC_CALL_THEN_WAIT]

    with open(os.devnull) as fobj:
        p = subprocess.Popen(cmd_1,
                             stdout=fobj,
                             stderr=fobj,
                             close_fds=True)

        time.sleep(2)

        subprocess.call(cmd_2,
                             stdout=fobj,
                             stderr=fobj,
                             close_fds=True)

        time.sleep(2)

        p.wait()


@step(u'Given there is no "([^"]*)" entry in queue "([^"]*)')
def given_there_is_no_event_entry_in_queue_log_table_in_queue_queue(step, event, queue_name):
    queuelog_manager.delete_event_by_queue(event, queue_name)


@step(u'Then i should see ([0-9]+) "([^"]*)" calls in queue "([^"]*)" in the queue log')
def then_i_should_see_nb_group1_calls_in_queue_group2_in_the_queue_log(step, expected_count, event, queue_name):
    count = queuelog_manager.get_event_count_queue(event, queue_name)

    assert(count == int(expected_count))


@step(u'Given I wait ([0-9]+) seconds for the dialplan to be reloaded')
def given_i_wait_5_seconds_for_the_dialplan_to_be_reloaded(step, count):
    time.sleep(int(count))
