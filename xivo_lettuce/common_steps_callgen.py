# -*- coding: UTF-8 -*-

import time
from lettuce.decorators import step
from lettuce.registry import world
from xivo_lettuce.manager import queuelog_manager
from xivo_lettuce.manager import statscall_manager
from xivo_ws.objects.user import UserLine, User
from utils.func import extract_number_and_context_from_extension
from xivo_lettuce.manager_ws import queue_manager_ws, agent_manager_ws, \
    user_manager_ws, line_manager_ws


@step(u'Given there is a user "([^"]*)" "([^"]*)" with extension "([^"]*)"')
def given_there_is_a_user_1_2(step, firstname, lastname, extension):
    number, context = extract_number_and_context_from_extension(extension)
    user_manager_ws.delete_user_with_firstname_lastname(firstname, lastname)
    line_manager_ws.delete_line_with_number(number, context)
    user_ids = [user.id for user in world.ws.users.search('%s %s' % (firstname, lastname))]
    for user_id in user_ids:
        world.ws.users.delete(user_id)
    u = User(firstname=firstname, lastname=lastname)
    u.line = UserLine(context=context, number=number)
    world.ws.users.add(u)
    given_i_wait_n_seconds(step, 5)


@step(u'Given there is no user "([^"]*)" "([^"]*)"$')
def given_there_is_no_user_with_number(step, firstname, lastname):
    user_manager_ws.delete_user_with_firstname_lastname(firstname, lastname)


@step(u'Given there is no queue with name "([^"]+)"$')
def given_there_is_no_queue_with_name(step, queue_name):
    queue_manager_ws.delete_queue_with_displayname(queue_name)


@step(u'Given there is no queue with name "([^"]+)" or number "([^"]*)"$')
def given_there_is_no_queue_with_name_or_number(step, queue_name, queue_number):
    queue_manager_ws.delete_queue_with_displayname(queue_name)
    queue_manager_ws.delete_queue_with_number(queue_number)


@step(u'Given there is no agent with number "([^"]*)"$')
def given_there_is_no_agent_with_number(step, agent_number):
    agent_manager_ws.delete_agent_with_number(agent_number)


@step(u'Given there is no "([A-Z_]+)" entry for agent "([^"]*)"')
def given_there_is_no_entry_for_agent(step, event, agent_number):
    queuelog_manager.delete_event_by_agent_number(event, agent_number)


@step(u'^Given there is no "([A-Z_]+)" entry in queue "(\S+)"$')
def given_there_is_no_entry_in_queue_queue(step, event, queue_name):
    queuelog_manager.delete_event_by_queue(event, queue_name)


@step(u'^Given there is no "([A-Z_]+)" entry in queue "(\S+)" between "(.+)" and "(.+)"$')
def given_there_is_no_event_entry_in_queue_log_table_in_queue_queue_between(step, event, queue_name, start, end):
    queuelog_manager.delete_event_by_queue_between(event, queue_name, start, end)


@step(u'Given I log agent "([^"]*)" on extension "([^"]*)"')
def given_i_log_the_phone(step, agent_number, extension):
    number, context = extract_number_and_context_from_extension(extension)
    lines = [line for line in world.ws.lines.search(number)]
    if not lines:
        assert(False)
    statscall_manager.execute_sip_register(lines[0].name, lines[0].secret)
    statscall_manager.execute_n_calls_then_wait(1, '*31%s' % agent_number, username=lines[0].name, password=lines[0].secret)


@step(u'Given I logout agent "([^"]*)" on extension "([^"]*)"')
def given_i_logout_the_phone(step, agent_number, extension):
    number, context = extract_number_and_context_from_extension(extension)
    lines = [line for line in world.ws.lines.search(number)]
    if not lines:
        assert(False)
    statscall_manager.execute_n_calls_then_wait(1, '*32%s' % agent_number, username=lines[0].name, password=lines[0].secret)


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
