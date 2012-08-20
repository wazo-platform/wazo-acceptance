# -*- coding: UTF-8 -*-

import time
from lettuce.decorators import step
from xivo_lettuce.manager import queuelog_manager, queue_manager, agent_manager, \
    user_manager
from xivo_lettuce.manager import stat_manager, statscall_manager
from lettuce.registry import world
from xivo_ws.objects.user import UserLine, User


@step(u'Given there is a queue "([^"]+)" in context "([^"]+)" with number "([^"]+)"$')
def given_there_is_a_queue_in_context_with_number(step, name, context, number):
    data = {'name': name,
            'number': number,
            'context': context,
            'maxlen': 0,
            'agents': ''}
    queue_manager.insert_queue(data)


@step(u'Given there is a queue "([^"]+)" in context "([^"]+)" with number "([^"]+)" with agent "([^"]*)"$')
def given_there_is_a_queue_in_context_with_number_with_agent(step, name, context, queue_number, agent_number):
    agent_id = agent_manager.find_agent_id_from_number(agent_number)
    data = {'name': name,
            'number': queue_number,
            'context': context,
            'maxlen': 0,
            'agents': agent_id}
    queue_manager.insert_queue(data)


@step(u'Given there is a agent "([^"]+)" "([^"]*)" in context "([^"]+)" with number "([^"]+)"$')
def given_there_is_a_agent_in_context_with_number(step, firstname, lastname, context, number):
    world.agent_id = agent_manager.insert_agent(firstname, lastname, number, '', context)


@step(u'Given there is a user "([^"]*)" "([^"]*)" in context "([^"]*)" with number "([^"]*)"')
def given_there_is_a_user_1_2(step, firstname, lastname, context, number):
    user_ids = [user.id for user in world.ws.users.search('%s %s' % (firstname, lastname))]
    for user_id in user_ids:
        world.ws.users.delete(user_id)
    u = User(firstname=firstname, lastname=lastname)
    u.line = UserLine(context=context, number=number)
    world.ws.users.add(u)


@step(u'Given there is no user "([^"]*)" "([^"]*)"')
def given_there_is_no_user_with_number(step, firstname, lastname):
    user_manager.delete_user(firstname, lastname)


@step(u'Given there is no queue with name "([^"]+)"')
def given_there_is_no_queue_with_name(step, queue_name):
    queue_manager.delete_queue_from_displayname(queue_name)


@step(u'Given there is no queue with number "([^"]*)"')
def given_there_is_no_queue_with_number(step, queue_number):
    queue_manager.delete_queue_from_number(queue_number)


@step(u'Given there is no agent with number "([^"]*)"')
def given_there_is_no_agent_with_number(step, agent_number):
    agent_manager.delete_agent_by_number(agent_number)


@step(u'Given there is no "([A-Z_]+)" entry for agent "([^"]*)"')
def given_there_is_no_entry_for_agent(step, event, agent_number):
    queuelog_manager.delete_event_by_agent_number(event, agent_number)


@step(u'^Given there is no "([A-Z_]+)" entry in queue "(\S+)"$')
def given_there_is_no_entry_in_queue_queue(step, event, queue_name):
    queuelog_manager.delete_event_by_queue(event, queue_name)


@step(u'^Given there is no "([A-Z_]+)" entry in queue "(\S+)" between "(.+)" and "(.+)"$')
def given_there_is_no_event_entry_in_queue_log_table_in_queue_queue_between(step, event, queue_name, start, end):
    queuelog_manager.delete_event_by_queue_between(event, queue_name, start, end)


@step(u'Then i should see ([0-9]+) "([^"]*)" event in queue "([^"]*)" in the queue log')
def then_i_should_see_nb_n_event_in_queue_in_the_queue_log(step, expected_count, event, queue_name):
    count = queuelog_manager.get_event_count_queue(event, queue_name)

    assert(count == int(expected_count))


@step(u'Then i should see ([0-9]+) "([^"]*)" event for agent "([^"]*)" in the queue log')
def then_i_should_see_n_event_for_agent_in_the_queue_log(step, expected_count, event, agent_number):
    count = queuelog_manager.get_event_count_agent(event, agent_number)

    assert(count == int(expected_count))


@step(u'Given I log agent "([^"]*)" on extension "([^"]*)"')
def given_i_log_the_phone(step, agent_number, extension):
    lines = [line for line in world.ws.lines.search(extension)]
    statscall_manager.execute_sip_register(lines[0].name, lines[0].secret)
    statscall_manager.execute_n_calls_to(1, '*31%s' % agent_number, lines[0].name, lines[0].secret)


@step(u'Given there is ([0-9]+) calls to extension "([^"]+)" and wait$')
def given_there_is_a_n_calls_to_extension_and_wait(step, count, number):
    statscall_manager.execute_n_calls_to(count, number, close='wait')


@step(u'Given there is ([0-9]+) calls to extension "([^"]+)"$')
def given_there_is_a_n_calls_to_extension_and_hangup(step, count, number):
    statscall_manager.execute_n_calls_to(count, number)


@step(u'Given I wait call then hangup after "([0-9]+)s"')
def given_i_wait_call_then_hangup_afert_x_seconds(step, call_duration):
    call_duration_ms = int(call_duration) * 1000
    statscall_manager.execute_answer_then_hangup(call_duration_ms)


@step(u'Given I wait call then wait')
def given_i_wait_call_then_wait(step):
    statscall_manager.execute_answer_then_wait()


@step(u'Given I wait ([0-9]+) seconds .*')
def given_i_wait_n_seconds(step, count):
    time.sleep(int(count))


@step(u'^Given there is a statistic configuration "(\S+)" from "([0-9:]+)" to "([0-9:]+)" with queue "(\S+)"$')
def given_there_is_a_configuration_with(step, config_name, start, end, queue_name):
    stat_manager.create_configuration(config_name, start, end, queue_name)


@step(u'^Given I have to following queue_log entries:$')
def given_i_have_the_following_queue_log_entries(step):
    queuelog_manager.insert_entries(step.hashes)


@step(u'^Given I clear and generate the statistics cache$')
def given_i_clear_and_generate_the_statistics_cache(step):
    stat_manager.regenerate_cache()


@step(u'^Then I should have the following statististics on "(.+)" on "(.+)" on configuration "(\S+)":$')
def then_i_should_have_stats_for_config(step, queue_name, day, config_name):
    print 'I should have', queue_name, day, config_name
    stat_manager.open_queue_stat_page_on_day(queue_name, day, config_name)
    stat_manager.check_queue_statistic(step.hashes)
