# -*- coding: UTF-8 -*-

from lettuce.decorators import step
from xivo_lettuce import sysutils, logs


@step(u'Asterisk command "([^"]*)" return no error')
def then_asterisk_command_group1_return_no_error(step, ast_cmd):
    command = ['asterisk', '-rx', '"%s"' % ast_cmd]
    assert sysutils.send_command(command)


@step(u'When I stop Asterisk')
def when_i_stop_asterisk(step):
    command = ['service', 'asterisk', 'stop']
    assert sysutils.send_command(command)


@step(u'When service "([^"]*)" run')
def then_service_group1_run(step, service):
    pidfile = sysutils.get_pidfile_for_service_name(service)
    assert sysutils.is_process_running(pidfile)


@step(u'I expected that the service "([^"]*)" restart')
def when_i_wait_service_service_group1_restart(step, service):
    pidfile = sysutils.get_pidfile_for_service_name(service)
    assert sysutils.wait_service_restart(pidfile)


@step(u'Then service "([^"]*)" not run')
def then_service_group1_not_run(step, service):
    pidfile = sysutils.get_pidfile_for_service_name(service)
    assert not sysutils.is_process_running(pidfile)


@step(u'Then I see in the log file service restarted by monit')
def then_i_see_in_the_log_file_servce_restarted_by_monit(step):
    logs.search_str_in_daemon_log('start: /usr/bin/xivo-service')
