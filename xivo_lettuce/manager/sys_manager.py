# -*- coding: UTF-8 -*-

from datetime import datetime, timedelta
from lettuce.registry import world
from utils.func import read_last_log_lines

SYSCONFD_LOGFILE = '/var/log/daemon.log'


def search_str_in_daemon_log(expression):
    min_timestamp = datetime.now() - timedelta(seconds=10)
    command = ['tail', '-n', '15', SYSCONFD_LOGFILE, '|', 'grep', 'sysconfd']
    result = world.ssh_client_xivo.out_call(command)

    loglines = read_last_log_lines(result.split('\n'), min_timestamp)
    for line in loglines:
        if expression in line:
            return True
    return False
