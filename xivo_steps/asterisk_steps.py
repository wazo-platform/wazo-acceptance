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

from lettuce import step
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
    command = ['service', 'asterisk', 'restart']
    sysutils.send_command(command)


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


@step(u'Then I see in the log file service restarted by monit')
def then_i_see_in_the_log_file_servce_restarted_by_monit(step):
    logs.search_str_in_daemon_log('start: /usr/bin/xivo-service')
