# -*- coding: utf-8 -*-
# Copyright 2013-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from datetime import datetime, timedelta
from hamcrest import assert_that
from hamcrest import close_to
from hamcrest import equal_to
from lettuce import step, world

from xivo_acceptance.helpers import stat_helper, queuelog_helper
from xivo_acceptance.lettuce import sysutils


@step(u'^Given there are a corrupt entry in queue_log$')
def given_there_are_a_corrupt_entry_in_queue_log(step):
    queuelog_helper.insert_corrupt_data()


@step(u'^Given there is a statistic configuration "(\S+)" from "([0-9:]+)" to "([0-9:]+)" with agent "(\S+)"$')
def given_there_is_a_configuration_with_agent(step, config_name, start, end, agent_number):
    stat_helper.add_configuration_with_agent(config_name, start, end, agent_number)


@step(u'^Given there is a statistic configuration "(\S+)" from "([0-9:]+)" to "([0-9:]+)" with queue "(\S+)"$')
def given_there_is_a_configuration_with(step, config_name, start, end, queue_name):
    stat_helper.add_configuration_with_queue(config_name, start, end, queue_name)


@step(u'^Given there is a statistic configuration "(\S+)" from "([0-9:]+)" to "([0-9:]+)" with queue "(\S+)" and agent "(\S+)"$')
def given_there_is_a_configuration_with_queue_and_agent(step, config_name, start, end, queue_name, agent_number):
    stat_helper.add_configuration_with_queue_and_agent(config_name, start, end, queue_name, agent_number)


@step(u'^Given there is a statistic configuration "(\S+)" from "([0-9:]+)" to "([0-9:]+)" with the following parameters:')
def given_there_is_a_configuration_with_the_following_parameters(step, config_name, start, end):
    entry = step.hashes[0]
    stat_helper.add_configuration_with_queue_and_agents(config_name, start, end, entry['queues'], entry['agents'])


@step(u'^Given I have the following queue_log entries:$')
def given_i_have_the_following_queue_log_entries(step):
    queuelog_helper.insert_entries(step.hashes)


@step(u'^Given I have the following queue_log entries in the last hour:$')
def given_i_have_to_following_queue_log_entries_in_the_last_hour(step):
    one_hour_ago = sysutils.xivo_current_datetime() - timedelta(hours=1)
    world.beginning_of_last_hour = one_hour_ago.replace(minute=0, second=0, microsecond=0)
    for entry in step.hashes:
        entry_time = datetime.strptime(entry['time'], "%M:%S.%f")
        last_hour_entry_time = entry_time.replace(year=one_hour_ago.year,
                                                  month=one_hour_ago.month,
                                                  day=one_hour_ago.day,
                                                  hour=one_hour_ago.hour)
        entry['time'] = last_hour_entry_time.strftime("%Y-%m-%d %H:%M:%S.%f")

    queuelog_helper.insert_entries(step.hashes)


@step(u'Given there is no "([A-Z_]+)" entry for agent "([^"]*)"')
def given_there_is_no_entry_for_agent(step, event, agent_number):
    queuelog_helper.delete_event_by_agent_number(event, agent_number)


@step(u'^Given there is no "([A-Z_]+)" entry in queue "(\S+)"$')
def given_there_is_no_entry_in_queue_queue(step, event, queue_name):
    queuelog_helper.delete_event_by_queue(event, queue_name)


@step(u'^Given there is no entries in queue_log between "(.+)" and "(.+)"$')
def given_there_is_no_entries_in_queue_log_table_between(step, start, end):
    queuelog_helper.delete_event_between(start, end)


@step(u'Given there is no entries in queue_log in the last hour')
def given_there_is_no_entries_in_queue_log_in_the_last_hour(step):
    current_hour = datetime.now().replace(minute=0, second=0, microsecond=0)
    last_hour = current_hour - timedelta(hours=1)

    queuelog_helper.delete_event_between(
        last_hour.strftime("%Y-%m-%d %H:%M:%S.%f"),
        datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    )


@step(u'Then i should see ([0-9]+) "([^"]*)" event in queue "([^"]*)" in the queue log')
def then_i_should_see_nb_n_event_in_queue_in_the_queue_log(step, expected_count, event, queue_name):
    count = queuelog_helper.get_event_count_queue(event, queue_name)

    assert_that(count, equal_to(int(expected_count)), 'Number of %s in %s' % (event, queue_name))


@step(u'Then i should see ([0-9]+) "([^"]*)" event for agent "([^"]*)" in the queue log')
def then_i_should_see_n_event_for_agent_in_the_queue_log(step, expected_count, event, agent_number):
    count = queuelog_helper.get_event_count_agent(event, agent_number)

    assert_that(count, equal_to(int(expected_count)), 'Number of %s for agent %s' % (event, agent_number))


@step(u'Then the queue_log table shows that agent "([^"]*)" has been logged for (\d+) seconds')
def then_the_queue_log_table_shows_that_agent_group1_has_been_logged_for_1_seconds(step, agent_number, expected_duration):
    login_duration = queuelog_helper.get_agent_last_login_duration(agent_number)
    assert_that(login_duration, close_to(int(expected_duration), 5))
