# -*- coding: UTF-8 -*-

from lettuce.decorators import step
from xivo_lettuce.manager import stat_manager, queuelog_manager, \
    statscall_manager
from xivo_lettuce.manager_ws import statconfs_manager_ws


@step(u'Given there are no calls running')
def given_there_are_no_calls_running(step):
    statscall_manager.killall_process_sipp()


@step(u'^Given there are a corrupt entry in queue_log$')
def given_there_are_a_corrupt_entry_in_queue_log(step):
    queuelog_manager.insert_corrupt_data()


@step(u'^Given there is a statistic configuration "(\S+)" from "([0-9:]+)" to "([0-9:]+)" with agent "(\S+)"$')
def given_there_is_a_configuration_with_agent(step, config_name, start, end, agent_number):
    statconfs_manager_ws.add_configuration_with_agent(config_name, start, end, agent_number)


@step(u'^Given there is a statistic configuration "(\S+)" from "([0-9:]+)" to "([0-9:]+)" with queue "(\S+)"$')
def given_there_is_a_configuration_with(step, config_name, start, end, queue_name):
    statconfs_manager_ws.add_configuration_with_queue(config_name, start, end, queue_name)


@step(u'^Given there is a statistic configuration "(\S+)" from "([0-9:]+)" to "([0-9:]+)" with queue "(\S+)" and agent "(\S+)"$')
def given_there_is_a_configuration_with_queue_and_agent(step, config_name, start, end, queue_name, agent_number):
    statconfs_manager_ws.add_configuration_with_queue_and_agent(config_name, start, end, queue_name, agent_number)


@step(u'^Given I have to following queue_log entries:$')
def given_i_have_the_following_queue_log_entries(step):
    queuelog_manager.insert_entries(step.hashes)


@step(u'^Given I clear and generate the statistics cache$')
def given_i_clear_and_generate_the_statistics_cache(step):
    stat_manager.regenerate_cache()


@step(u'^When execute xivo-stat$')
def when_execute_xivo_stats(step):
    stat_manager.generate_cache()


@step('^Then I don\'t should not have an error$')
def then_i_dont_should_not_have_error(step):
    pass


@step(u'Then i should see ([0-9]+) "([^"]*)" event in queue "([^"]*)" in the queue log')
def then_i_should_see_nb_n_event_in_queue_in_the_queue_log(step, expected_count, event, queue_name):
    count = queuelog_manager.get_event_count_queue(event, queue_name)

    assert(count == int(expected_count))


@step(u'Then i should see ([0-9]+) "([^"]*)" event for agent "([^"]*)" in the queue log')
def then_i_should_see_n_event_for_agent_in_the_queue_log(step, expected_count, event, agent_number):
    count = queuelog_manager.get_event_count_agent(event, agent_number)

    assert(count == int(expected_count))


@step(u'Then the last event "([A-Z]+)" for agent "([^"]*)" should not have a callid "([^"]*)"')
def then_the_last_event_for_agent_should_not_have_a_callid(step, event, agent, callid):
    result = queuelog_manager.get_last_callid(event, agent)

    assert(result != callid)


@step(u'^Then I should have the following statististics on "(.+)" on "(.+)" on configuration "(\S+)":$')
def then_i_should_have_stats_for_config(step, queue_name, day, config_name):
    stat_manager.open_queue_stat_page_on_day(queue_name, day, config_name)
    stat_manager.check_queue_statistic(step.hashes)


@step(u'^Then I should have the following statististics on agent "(.+)" on "(.+)" on configuration "(\S+)":$')
def then_i_should_have_stats_on_agent_for_config(step, agent_number, day, config_name):
    stat_manager.open_agent_stat_page_on_day(agent_number, day, config_name)
    stat_manager.check_agent_statistic(step.hashes)
