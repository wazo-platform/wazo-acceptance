# -*- coding: UTF-8 -*-

from lettuce.decorators import step

from lettuce import world
from xivo_lettuce import terrain
from xivo_lettuce.common_steps_callgen import *
from xivo_lettuce.common_steps_webi import *
from xivo_lettuce.manager import queuelog_manager, stat_manager


@step(u'Then i should see ([0-9]+) "([^"]*)" event in queue "([^"]*)" in the queue log')
def then_i_should_see_nb_n_event_in_queue_in_the_queue_log(step, expected_count, event, queue_name):
    count = queuelog_manager.get_event_count_queue(event, queue_name)

    assert(count == int(expected_count))


@step(u'Then i should see ([0-9]+) "([^"]*)" event for agent "([^"]*)" in the queue log')
def then_i_should_see_n_event_for_agent_in_the_queue_log(step, expected_count, event, agent_number):
    count = queuelog_manager.get_event_count_agent(event, agent_number)

    assert(count == int(expected_count))


@step(u'^Given there is a statistic configuration "(\S+)" from "([0-9:]+)" to "([0-9:]+)" with queue "(\S+)"$')
def given_there_is_a_configuration_with(step, config_name, start, end, queue_name):
    stat_manager.create_configuration(config_name, start, end, queue_name)


@step(u'^Given there is a statistic configuration "(\S+)" from "([0-9:]+)" to "([0-9:]+)" with queue "(\S+)" and agent "(\S+)"$')
def given_there_is_a_configuration_with_queue_and_agent(step, config_name, start, end, queue_name, agent_number):
    stat_manager.create_configuration(config_name, start, end, queue_name, agent_number)


@step(u'^Given I have to following queue_log entries:$')
def given_i_have_the_following_queue_log_entries(step):
    queuelog_manager.insert_entries(step.hashes)


@step(u'^Given I clear and generate the statistics cache$')
def given_i_clear_and_generate_the_statistics_cache(step):
    stat_manager.regenerate_cache()


@step(u'^Then I should have the following statististics on "(.+)" on "(.+)" on configuration "(\S+)":$')
def then_i_should_have_stats_for_config(step, queue_name, day, config_name):
    stat_manager.open_queue_stat_page_on_day(queue_name, day, config_name)
    stat_manager.check_queue_statistic(step.hashes)


@step(u'^Then I should have the following statististics on agent "(.+)" on "(.+)" on configuration "(\S+)":$')
def then_i_should_have_stats_on_agent_for_config(step, agent_number, day, config_name):
    stat_manager.open_agent_stat_page_on_day(agent_number, day, config_name)
    stat_manager.check_agent_statistic(step.hashes)
