# -*- coding: UTF-8 -*-

from datetime import datetime, timedelta
from lettuce.registry import world
from utils.func import read_last_log_lines

SYSCONFD_LOGFILE = '/var/log/daemon.log'
ASTERISK_LOGFILE = '/var/log/asterisk/messages'


def search_str_in_daemon_log(expression, delta=10):
    return _search_str_in_log_file(SYSCONFD_LOGFILE, expression, delta)


def search_str_in_asterisk_log(expression, delta=10):
    return _search_str_in_log_file(ASTERISK_LOGFILE, expression, delta)


def _search_str_in_log_file(logfile, expression, delta=10):
    command = ['tail', '-n', '15', logfile]
    result = world.ssh_client_xivo.out_call(command)

    min_timestamp = datetime.now() - timedelta(seconds=delta)
    loglines = read_last_log_lines(result.split('\n'), min_timestamp)

    for line in loglines:
        if expression in line:
            return True
    return False
