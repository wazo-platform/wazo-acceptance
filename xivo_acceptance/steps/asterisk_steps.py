# -*- coding: utf-8 -*-

# Copyright (C) 2013-2016 Avencall
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

import os
import re
import time

from datetime import timedelta

from hamcrest import assert_that
from hamcrest import contains
from hamcrest import equal_to
from hamcrest import has_entries
from hamcrest import has_item
from hamcrest import has_items
from hamcrest import not_
from lettuce import step, registry
from xivo_acceptance.helpers import asterisk_helper, file_helper
from xivo_acceptance.helpers import line_read_helper
from xivo_acceptance.lettuce import asterisk, sysutils, logs, common


@step(u'Given the AMI is monitored')
def given_the_ami_is_monitored(step):
    asterisk.start_ami_monitoring()


@step(u'Asterisk command "([^"]*)" return no error')
def then_asterisk_command_group1_return_no_error(step, ast_cmd):
    command = ['asterisk', '-rx', '"%s"' % ast_cmd]
    assert sysutils.send_command(command)


@step(u'When I stop Asterisk')
def when_i_stop_asterisk(step):
    command = ['service', 'asterisk', 'stop']
    assert sysutils.send_command(command)


@step(u'When I start Asterisk')
def when_i_start_asterisk(step):
    command = ['service', 'asterisk', 'start']
    assert sysutils.send_command(command)


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


@step(u'Then I see in the AMI that the line "([^"]*)" has been synchronized')
def then_i_see_in_the_ami_that_the_line_group1_has_been_synchronized(step, extension):
    line = line_read_helper.find_with_extension(extension)
    line_name = line['name']
    lines = [
        'Action: SIPnotify',
        'Channel: %s' % line_name,
        'Variable: Event=check-sync',
    ]

    def _assert():
        ami_lines = asterisk.fetch_ami_lines()
        assert_that(ami_lines, has_items(*lines))

    common.wait_until_assert(_assert, tries=3)


@step(u'Given I change the "([^"]*)" AMI password to "([^"]*)"')
def given_i_change_the_user_ami_password_to_passwd(step, user, passwd):
    content = '''\
[{user}]
secret = {password}
deny=0.0.0.0/0.0.0.0
permit=127.0.0.1/255.255.255.0
write = system
'''.format(user=user, password=passwd)
    filename = '/etc/asterisk/manager.d/monit.conf'

    temp_filename = file_helper.write_remote_file(filename, content, user='asterisk')
    asterisk_helper.send_to_asterisk_cli('manager reload')

    def cleanup(*args, **kwargs):
        registry.CALLBACK_REGISTRY['scenario']['after_each'].pop(-1)
        file_helper.remove_remote_file(filename)
        try:
            os.unlink(temp_filename)
        except OSError:
            # file does not exists
            pass
        asterisk_helper.send_to_asterisk_cli('manager reload')

    registry.CALLBACK_REGISTRY['scenario']['after_each'].append(cleanup)


@step(u'Then asterisk should be restarted in the following "([^"]*)" minutes')
def then_asterisk_should_be_restarted_in_the_following_n_minutes(step, n):
    beginning_uptime = _get_asterisk_uptime()
    assert beginning_uptime is not None, 'Asterisk is not started'

    start = time.time()
    max_wait = n * 60
    while time.time() - start < max_wait:
        uptime = _get_asterisk_uptime()
        if uptime and uptime < beginning_uptime:
            return
        time.sleep(1)

    assert False, 'Asterisk has not been restart in less that %s minutes' % n


@step(u'Then extension "([^"]*)" is not in context "([^"]*)"')
def then_extension_is_not_in_context(step, extension, context):
    in_context = _extension_in_context(extension, context)
    common.wait_until_assert(lambda: assert_that(not_(in_context)), tries=3)


@step(u'Then extension "([^"]*)" is in context "([^"]*)"')
def then_extension_is_in_context(step, extension, context):
    in_context = _extension_in_context(extension, context)
    common.wait_until_assert(lambda: assert_that(not_(in_context)), tries=3)


def _get_asterisk_uptime():
    output = asterisk_helper.check_output_asterisk_cli('core show uptime')

    pattern_week = re.compile(r'System uptime: (\d)+ week[s]?, (\d+) hour[s]?, (\d+) minute[s]?, (\d+) second[s]?')
    values = pattern_week.match(output)
    if values:
        return timedelta(weeks=int(values.group(1)),
                         days=int(values.group(2)),
                         hours=int(values.group(3)),
                         minutes=int(values.group(4)),
                         seconds=int(values.group(5)))

    pattern_day = re.compile(r'System uptime: (\d+) day[s]?, (\d+) hour[s]?, (\d+) minute[s]?, (\d+) second[s]?')
    values = pattern_day.match(output)
    if values:
        return timedelta(days=int(values.group(1)),
                         hours=int(values.group(2)),
                         minutes=int(values.group(3)),
                         seconds=int(values.group(4)))

    pattern_hour = re.compile(r'System uptime: (\d+) hour[s]?, (\d+) minute[s]?, (\d+) second[s]?')
    values = pattern_hour.match(output)
    if values:
        return timedelta(hours=int(values.group(1)),
                         minutes=int(values.group(2)),
                         seconds=int(values.group(3)))

    pattern_minute = re.compile(r'System uptime: (\d+) minute[s]?, (\d+) second[s]?')
    values = pattern_minute.match(output)
    if values:
        return timedelta(minutes=int(values.group(1)),
                         seconds=int(values.group(2)))

    pattern_second = re.compile(r'System uptime: (\d+) second[s]?')
    values = pattern_second.match(output)
    if values:
        return timedelta(seconds=int(values.group(1)))

    return None


def _extension_in_context(extension, context):
    asterisk_cmd = 'dialplan show {}@{}'.format(extension, context)
    command = ['asterisk', '-rx', '"{}"'.format(asterisk_cmd)]

    output = sysutils.output_command(command)

    return 'There is no existence of' not in output


@step('Then I have the following hints')
def then_i_have_the_following_hints(step):
    actual_hints = _list_hints()

    for expected_hint in step.hashes:
        assert_that(actual_hints, has_item(has_entries(expected_hint)))


def _list_hints():
    asterisk_cmd = 'core show hints'
    command = ['asterisk', '-rx', '"{}"'.format(asterisk_cmd)]

    output = sysutils.output_command(command).split('\n')
    output = output[2:-3]  # strip header and footer
    return [_parse_hint(line) for line in output]


def _parse_hint(line):
    hint = {}
    hint['exten'] = line[:20].strip()
    hint['line'] = line[22:44].strip()
    return hint
