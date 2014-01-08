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

import time

from hamcrest import assert_that, equal_to, contains
from lettuce import step, world
from xivo_acceptance.helpers import asterisk_helper
from xivo_lettuce import sysutils, logs


@step(u'Asterisk command "([^"]*)" return no error')
def then_asterisk_command_group1_return_no_error(step, ast_cmd):
    command = ['asterisk', '-rx', '"%s"' % ast_cmd]
    assert sysutils.send_command(command)


@step(u'When I stop Asterisk')
def when_i_stop_asterisk(step):
    command = ['service', 'asterisk', 'stop']
    assert sysutils.send_command(command)


@step(u'When I restart Asterisk')
def when_i_restart_asterisk(step):
    sysutils.restart_service('asterisk')


@step(u'When I wait for the service "([^"]*)" to stop')
def when_i_wait_for_the_service_group1_to_stop(step, service):
    pidfile = sysutils.get_pidfile_for_service_name(service)
    sysutils.wait_service_successfully_stopped(pidfile)


@step(u'When I wait for the service "([^"]*)" to restart')
def when_i_wait_for_the_service_group1_to_restart(step, service):
    pidfile = sysutils.get_pidfile_for_service_name(service)
    assert sysutils.wait_service_successfully_started(pidfile)


@step(u'Then the service "([^"]*)" is running')
def then_the_service_group1_is_running(step, service):
    pidfile = sysutils.get_pidfile_for_service_name(service)
    assert sysutils.is_process_running(pidfile)


@step(u'Then the service "([^"]*)" is no longer running')
def then_the_service_group1_is_no_longer_running(step, service):
    pidfile = sysutils.get_pidfile_for_service_name(service)
    assert not sysutils.is_process_running(pidfile)


@step(u'Given I check the number of file descriptor for asterisk')
def given_i_check_the_number_of_file_descriptor_for_asterisk(step):
    fd_count = sysutils.get_number_of_file_descriptor('asterisk')
    world.asterisk_fd_count = fd_count


@step(u'When I reload the module chan_sccp.so')
def when_i_reload_the_module_chan_sccp_so(step):
    ast_cmd = 'module reload chan_sccp.so'
    command = ['asterisk', '-rx', '"%s"' % ast_cmd]
    assert sysutils.send_command(command)
    time.sleep(3)


@step(u'Then I should have the same number of open file descriptor')
def then_i_should_have_the_same_number_of_open_file_descriptor(step):
    fd_count = sysutils.get_number_of_file_descriptor('asterisk')
    assert_that(fd_count, equal_to(world.asterisk_fd_count), 'Number of file descriptor')


@step(u'Then I see in the log file service restarted by monit')
def then_i_see_in_the_log_file_servce_restarted_by_monit(step):
    logs.search_str_in_daemon_log('start: /usr/bin/xivo-service')


@step(u'Then the "([^"]*)" section of "([^"]*)" contains the options:')
def then_the_group1_section_of_group2_contains(step, section, filename):
    option_names = [item['name'] for item in step.hashes]
    expected_options = [(item['name'], item['value']) for item in step.hashes]

    options = asterisk_helper.get_conf_options(filename, section, option_names)

    assert_that(options, contains(*expected_options))


@step(u'Then the "([^"]*)" section of "([^"]*)" does not contain the options:')
def then_the_group1_section_of_group2_does_not_contain_the_options(step, section, filename):
    option_names = [item['name'] for item in step.hashes]

    options = asterisk_helper.get_conf_options(filename, section, option_names)

    assert_that(options, equal_to([]))
