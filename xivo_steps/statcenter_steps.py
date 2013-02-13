# -*- coding: utf-8 -*-

# Copyright (C) 2013 Avencall
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

from datetime import datetime
from datetime import timedelta
from lettuce import step
from hamcrest import assert_that, equal_to
from xivo_lettuce.manager import stat_manager, queuelog_manager
from xivo_lettuce.manager_ws import statconfs_manager_ws


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


@step(u'^Given I have the following queue_log entries:$')
def given_i_have_the_following_queue_log_entries(step):
    queuelog_manager.insert_entries(step.hashes)


@step(u'^Given I have the following queue_log entries in the last hour:$')
def given_i_have_to_following_queue_log_entries_in_the_last_hour(step):
    now = datetime.now()
    last_hour = datetime(now.year, now.month, now.day, now.hour - 1, 0, 0, 0)
    for entry in step.hashes:
        t = datetime.strptime(entry['time'], "%M:%S.%f")
        offset = timedelta(minutes=t.minute, seconds=t.second, microseconds=t.microsecond)
        entry['time'] = (last_hour + offset).strftime("%Y-%m-%d %H:%M:%S.%f")

    queuelog_manager.insert_entries(step.hashes)


@step(u'^Given I clear and generate the statistics cache$')
def given_i_clear_and_generate_the_statistics_cache(step):
    stat_manager.regenerate_cache()


@step(u'^Given I clear and generate the statistics cache twice$')
def given_i_clear_and_generate_the_statistics_cache_twice(step):
    stat_manager.regenerate_cache()
    stat_manager.generate_cache()


@step(u'^When execute xivo-stat$')
def when_execute_xivo_stats(step):
    stat_manager.generate_cache()


@step('^Then I don\'t should not have an error$')
def then_i_dont_should_not_have_error(step):
    pass


@step(u'Then i should see ([0-9]+) "([^"]*)" event in queue "([^"]*)" in the queue log')
def then_i_should_see_nb_n_event_in_queue_in_the_queue_log(step, expected_count, event, queue_name):
    count = queuelog_manager.get_event_count_queue(event, queue_name)

    assert_that(count, equal_to(int(expected_count)))


@step(u'Then i should see ([0-9]+) "([^"]*)" event for agent "([^"]*)" in the queue log')
def then_i_should_see_n_event_for_agent_in_the_queue_log(step, expected_count, event, agent_number):
    count = queuelog_manager.get_event_count_agent(event, agent_number)

    assert_that(count, equal_to(int(expected_count)))


@step(u'^Then I should have the following statististics on "(.+)" on "(.+)" on configuration "(\S+)":$')
def then_i_should_have_stats_for_config(step, queue_name, day, config_name):
    stat_manager.open_queue_stat_page_on_day(queue_name, day, config_name)
    stat_manager.check_queue_statistic(step.hashes)


@step(u'^Then I should have the following statististics on agent "(.+)" on "(.+)" on configuration "(\S+)":$')
def then_i_should_have_stats_on_agent_for_config(step, agent_number, day, config_name):
    stat_manager.open_agent_stat_page_on_day(agent_number, day, config_name)
    stat_manager.check_agent_statistic(step.hashes)


@step(u'Then I should have "([^"]*)" minutes login in the last hour on agent "([^"]*)" on configuration "([^"]*)":')
def then_i_should_have_group1_minutes_login_in_the_last_hour_on_agent_group2_on_configuration_group3(step, login_time, agent_number, config_name):
    now = datetime.now()
    day = datetime(now.year, now.month, now.day)
    stat_manager.open_agent_stat_page_on_day(agent_number, day, config_name)

    hour = datetime(now.year, now.month, now.day, now.hour - 1, 0, 0, 0)
    stat_manager.check_agent_login_time(login_time, hour)
