# -*- coding: UTF-8 -*-

import re
from datetime import datetime, timedelta
from lettuce.registry import world

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
    loglines = _get_lines_since_timestamp(result, min_timestamp)

    for line in loglines:
        if expression in line:
            return True
    return False


def _get_lines_since_timestamp(text,
                        min_timestamp,
                        date_format="%b %d %H:%M:%S",
                        date_pattern="([\w]{3} [\d ]{2} [\d]{2}:[\d]{2}:[\d]{2})"):
    lines = text.split("\n")
    date_match = re.compile(date_pattern, re.I)

    res = []
    for line in lines:
        try:
            m = date_match.search(line)
            datetext = m.group(1)
        except (AttributeError, IndexError):
            continue
        timestamp = datetime.strptime(datetext, date_format)
        timestamp = _add_year_to_datetime(timestamp)

        if timestamp >= min_timestamp:
            res.append(line)

    return res


def _add_year_to_datetime(ts, year=None):
    year = year or datetime.now().year
    timestamp = datetime(
        year=year,
        month=ts.month,
        day=ts.day,
        hour=ts.hour,
        minute=ts.minute,
        second=ts.second)

    return timestamp
