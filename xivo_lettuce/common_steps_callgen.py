# -*- coding: UTF-8 -*-

import time
from lettuce.decorators import step
from lettuce.registry import world
from xivo_lettuce.manager import queuelog_manager
from xivo_lettuce.manager import statscall_manager
from utils.func import extract_number_and_context_from_extension
from datetime import datetime


@step(u'Given there is no "([A-Z_]+)" entry for agent "([^"]*)"')
def given_there_is_no_entry_for_agent(step, event, agent_number):
    queuelog_manager.delete_event_by_agent_number(event, agent_number)


@step(u'^Given there is no "([A-Z_]+)" entry in queue "(\S+)"$')
def given_there_is_no_entry_in_queue_queue(step, event, queue_name):
    queuelog_manager.delete_event_by_queue(event, queue_name)


@step(u'^Given there is no "([A-Z_]+)" entry in queue "(\S+)" between "(.+)" and "(.+)"$')
def given_there_is_no_event_entry_in_queue_log_table_in_queue_between(step, event, queue_name, start, end):
    queuelog_manager.delete_event_by_queue_between(event, queue_name, start, end)


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


@step(u'Given I register extension "([^"]*)"')
def given_i_register_extension(step, extension):
    number, context = extract_number_and_context_from_extension(extension)
    lines = [line for line in world.ws.lines.search(number)]
    if not lines:
        assert(False)
    statscall_manager.execute_sip_register(lines[0].name, lines[0].secret)


@step(u'Given I log agent "([^"]*)" on extension "([^"]*)"')
def given_i_log_the_phone(step, agent_number, extension):
    number, context = extract_number_and_context_from_extension(extension)
    lines = [line for line in world.ws.lines.search(number)]
    if not lines:
        assert(False)
    statscall_manager.execute_sip_register(lines[0].name, lines[0].secret)
    statscall_manager.execute_n_calls_then_wait(1, '*31%s' % agent_number, username=lines[0].name, password=lines[0].secret)
    world.logged_agents.append(agent_number)


@step(u'Given I logout agent "([^"]*)" on extension "([^"]*)"')
def given_i_logout_the_phone(step, agent_number, extension):
    number, context = extract_number_and_context_from_extension(extension)
    lines = [line for line in world.ws.lines.search(number)]
    if not lines:
        assert(False)
    statscall_manager.execute_n_calls_then_wait(1, '*32%s' % agent_number, username=lines[0].name, password=lines[0].secret)


@step(u'Given there are no calls running')
def given_there_are_no_calls_running(step):
    statscall_manager.killall_process_sipp()


@step(u'Given there is ([0-9]+) calls to extension "([^"]+)" and wait$')
def given_there_is_n_calls_to_extension_and_wait(step, count, extension):
    statscall_manager.execute_n_calls_then_wait(count, extension)


@step(u'When i call extension "([^"]+)"$')
def when_i_call_extension(step, extension):
    statscall_manager.execute_n_calls_then_wait(1, extension)


@step(u'Given there is ([0-9]+) calls to extension "([^"]+)"$')
def given_there_is_n_calls_to_extension_and_hangup(step, count, extension):
    statscall_manager.execute_n_calls_then_hangup(count, extension)


@step(u'Given there is ([0-9]+) calls to extension "([^"]*)" then i hang up after "([0-9]+)s"')
def given_there_is_n_calls_to_extension_then_i_hangup_after_n_seconds(step, count, extension, call_duration):
    call_duration_ms = int(call_duration) * 1000
    statscall_manager.execute_n_calls_then_hangup(count, extension, duration=call_duration_ms)


@step(u'Given I wait call then i answer and wait')
def given_i_wait_call_then_i_answer_then_i_answer_and_wait(step):
    statscall_manager.execute_answer_then_wait()


@step(u'Given I wait call then i answer then i hang up after "([0-9]+)s"')
def given_i_wait_call_then_i_answer_then_hangup_after_n_seconds(step, call_duration):
    call_duration_ms = int(call_duration) * 1000
    statscall_manager.execute_answer_then_hangup(call_duration_ms)


@step(u'Given I wait call then i answer after "([0-9]+)s" then i hang up after "([0-9]+)s"')
def given_i_wait_call_then_answer_after_x_seconds_then_i_hangup_after_n_second(step, ring_time, call_duration):
    ring_time_ms = int(ring_time) * 1000
    call_duration_ms = int(call_duration) * 1000
    statscall_manager.execute_answer_then_hangup(call_duration_ms, ring_time_ms)


@step(u'Given I wait call then i answer after "([0-9]+)s" then i wait')
def given_i_wait_then_i_answer_after_n_second_then_i_wait(step, ring_time):
    ring_time_ms = int(ring_time) * 1000
    statscall_manager.execute_answer_then_wait(ring_time_ms)


@step(u'When I wait ([0-9]+) seconds .*')
@step(u'Given I wait ([0-9]+) seconds .*')
def given_i_wait_n_seconds(step, count):
    time.sleep(int(count))
