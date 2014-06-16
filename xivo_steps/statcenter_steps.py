# -*- coding: utf-8 -*-

# Copyright (C) 2013-2014 Avencall
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

from datetime import date, datetime, timedelta
from hamcrest import *
from lettuce import step, world

from xivo_acceptance.action.webi import stat as stat_action_webi
from xivo_acceptance.helpers import stat_helper, queuelog_helper


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
    one_hour_ago = datetime.now() - timedelta(hours=1)
    world.beginning_of_last_hour = one_hour_ago.replace(minute=0, second=0, microsecond=0)
    for entry in step.hashes:
        entry_time = datetime.strptime(entry['time'], "%M:%S.%f")
        last_hour_entry_time = entry_time.replace(year=one_hour_ago.year,
                                                  month=one_hour_ago.month,
                                                  day=one_hour_ago.day,
                                                  hour=one_hour_ago.hour)
        entry['time'] = last_hour_entry_time.strftime("%Y-%m-%d %H:%M:%S.%f")

    queuelog_helper.insert_entries(step.hashes)


@step(u'^Given I clear and generate the statistics cache$')
def given_i_clear_and_generate_the_statistics_cache(step):
    stat_action_webi.regenerate_cache()


@step(u'^Given I clear the statistics cache$')
def given_i_clear_the_statistics_cache(step):
    stat_action_webi.clean_cache()


@step(u'^Given I generate the statistics cache from start time "([^"]*)"$')
def given_i_generate_the_statistics_cache_from_start_time(step, start_time):
    stat_action_webi.generate_cache(start_time)


@step(u'Given I generate the statistics cache from start time "([^"]*)" to end time "([^"]*)"')
def given_i_generate_the_statistics_cache_from_start_time_group1_to_end_time_group2(step, start_time, end_time):
    stat_action_webi.generate_cache(start_time, end_time)


@step(u'^Given I clear and generate the statistics cache twice$')
def given_i_clear_and_generate_the_statistics_cache_twice(step):
    stat_action_webi.regenerate_cache()
    stat_action_webi.generate_cache()


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


@step(u'^When execute xivo-stat$')
def when_execute_xivo_stats(step):
    stat_action_webi.generate_cache()


@step('^Then I don\'t should not have an error$')
def then_i_dont_should_not_have_error(step):
    pass


@step(u'Then i should see ([0-9]+) "([^"]*)" event in queue "([^"]*)" in the queue log')
def then_i_should_see_nb_n_event_in_queue_in_the_queue_log(step, expected_count, event, queue_name):
    count = queuelog_helper.get_event_count_queue(event, queue_name)

    assert_that(count, equal_to(int(expected_count)), 'Number of %s in %s' % (event, queue_name))


@step(u'Then i should see ([0-9]+) "([^"]*)" event for agent "([^"]*)" in the queue log')
def then_i_should_see_n_event_for_agent_in_the_queue_log(step, expected_count, event, agent_number):
    count = queuelog_helper.get_event_count_agent(event, agent_number)

    assert_that(count, equal_to(int(expected_count)), 'Number of %s for agent %s' % (event, agent_number))


@step(u'^Then I should have the following statistics on "(.+)" on "(.+)" on configuration "(\S+)":$')
def then_i_should_have_stats_for_config(step, queue_name, day, config_name):
    stat_action_webi.open_queue_stat_page_on_day(queue_name, day, config_name)
    stat_action_webi.check_queue_statistic(step.hashes)


@step(u'^Then I should have the following statistics on agent "(.+)" on "(.+)" on configuration "(\S+)":$')
def then_i_should_have_stats_on_agent_for_config(step, agent_number, day, config_name):
    stat_action_webi.open_agent_stat_page_on_day(agent_number, day, config_name)
    stat_action_webi.check_agent_statistic(step.hashes)


@step(u'Then I should have "([^"]*)" minutes login in the last hour on agent "([^"]*)" on configuration "([^"]*)":')
def then_i_should_have_group1_minutes_login_in_the_last_hour_on_agent_group2_on_configuration_group3(step, login_time, agent_number, config_name):
    day_of_last_hour = date(world.beginning_of_last_hour.year,
                            world.beginning_of_last_hour.month,
                            world.beginning_of_last_hour.day)
    stat_action_webi.open_agent_stat_page_on_day(agent_number, day_of_last_hour, config_name)

    stat_action_webi.check_agent_login_time(login_time, world.beginning_of_last_hour)
