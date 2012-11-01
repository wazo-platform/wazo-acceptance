# -*- coding: UTF-8 -*-

import time
from datetime import datetime
from lettuce import step
from xivo_lettuce.manager import queuelog_manager
from xivo_lettuce.manager import call_manager, agent_status_manager
from xivo_lettuce.manager_ws.line_manager_ws import find_line_with_extension


@step(u'Given there is no "([A-Z_]+)" entry for agent "([^"]*)"')
def given_there_is_no_entry_for_agent(step, event, agent_number):
    queuelog_manager.delete_event_by_agent_number(event, agent_number)


@step(u'^Given there is no "([A-Z_]+)" entry in queue "(\S+)"$')
def given_there_is_no_entry_in_queue_queue(step, event, queue_name):
    queuelog_manager.delete_event_by_queue(event, queue_name)


@step(u'^Given there is no entries in queue_log between "(.+)" and "(.+)"$')
def given_there_is_no_entries_in_queue_log_table_between(step, start, end):
    queuelog_manager.delete_event_between(start, end)


@step(u'Given there is no entries in queue_log in the last hour')
def given_there_is_no_entries_in_queue_log_in_the_last_hour(step):
    now = datetime.now()
    last_hour = datetime(now.year, now.month, now.day, now.hour - 1, 0, 0, 0)

    queuelog_manager.delete_event_between(
        last_hour.strftime("%Y-%m-%d %H:%M:%S.%f"),
        now.strftime("%Y-%m-%d %H:%M:%S.%f")
    )


@step(u'I register extension "([^"]*)"')
def i_register_extension(step, extension):
    line = find_line_with_extension(extension)
    call_manager.execute_sip_register(line.name, line.secret)


@step(u'Given I log agent "([^"]*)" on extension "([^"]*)"')
def given_i_log_the_phone(step, agent_number, extension):
    agent_status_manager.log_agent(agent_number, extension)


@step(u'Given I logout agent "([^"]*)" on extension "([^"]*)"')
def given_i_logout_the_phone(step, agent_number, extension):
    agent_status_manager.unlog_agent(agent_number, extension)


@step(u'Given there are no calls running')
def given_there_are_no_calls_running(step):
    call_manager.killall_process_sipp()


@step(u'there is ([0-9]+) calls to extension "([^"]+)" and wait$')
def there_is_n_calls_to_extension_and_wait(step, count, extension):
    call_manager.execute_n_calls_then_wait(count, extension)


@step(u'When there is ([0-9]+) calls to extension "([^"]+)" on trunk "([^"]+)" and wait$')
def given_there_is_n_calls_to_extension_on_trunk_and_wait(step, count, extension, trunk_name):
    call_manager.execute_n_calls_then_wait(count,
                                           extension,
                                           username=trunk_name,
                                           password=trunk_name)


@step(u'When I call extension "([^"]+)"$')
def when_i_call_extension(step, extension):
    call_manager.execute_n_calls_then_wait(1, extension)


@step(u'Given there is ([0-9]+) calls to extension "([^"]+)"$')
def given_there_is_n_calls_to_extension_and_hangup(step, count, extension):
    call_manager.execute_n_calls_then_hangup(count, extension)


@step(u'Given there is ([0-9]+) calls to extension "([^"]*)" then i hang up after "([0-9]+)s"')
def given_there_is_n_calls_to_extension_then_i_hangup_after_n_seconds(step, count, extension, call_duration):
    call_duration_ms = int(call_duration) * 1000
    call_manager.execute_n_calls_then_hangup(count, extension, duration=call_duration_ms)


@step(u'Given I wait call then I answer and wait')
def given_i_wait_call_then_i_answer_then_i_answer_and_wait(step):
    call_manager.execute_answer_then_wait()


@step(u'Given I wait call then I answer then I hang up after "([0-9]+)s"')
def given_i_wait_call_then_i_answer_then_hangup_after_n_seconds(step, call_duration):
    call_duration_ms = int(call_duration) * 1000
    call_manager.execute_answer_then_hangup(call_duration_ms)


@step(u'I wait (\d+) seconds')
def given_i_wait_n_seconds(step, count):
    time.sleep(int(count))
