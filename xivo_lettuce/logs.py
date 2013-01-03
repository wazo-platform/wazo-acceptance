# -*- coding: UTF-8 -*-

import re

from collections import namedtuple
from datetime import datetime, timedelta
from lettuce.registry import world

DAEMON_LOGFILE = '/var/log/daemon.log'
ASTERISK_LOGFILE = '/var/log/asterisk/messages'
XIVO_AGENT_LOGFILE = '/var/log/xivo-agentd.log'

DAEMON_DATE_FORMAT = "%b %d %H:%M:%S"
DAEMON_DATE_PATTERN = "([\w]{3} [\d ]{2} [\d]{2}:[\d]{2}:[\d]{2})"

XIVO_AGENT_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
XIVO_AGENT_DATE_PATTERN = r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}"

LogfileInfo = namedtuple('LogfileInfo', ['logfile', 'date_format', 'date_pattern'])

DAEMON_LOG_INFO = LogfileInfo(logfile=DAEMON_LOGFILE,
                              date_format=DAEMON_DATE_FORMAT,
                              date_pattern=DAEMON_DATE_PATTERN)

ASTERISK_LOG_INFO = LogfileInfo(logfile=ASTERISK_LOGFILE,
                                date_format=DAEMON_DATE_FORMAT,
                                date_pattern=DAEMON_DATE_PATTERN)

XIVO_AGENT_LOG_INFO = LogfileInfo(logfile=XIVO_AGENT_LOGFILE,
                                  date_format=XIVO_AGENT_DATE_FORMAT,
                                  date_pattern=XIVO_AGENT_DATE_PATTERN)


def search_str_in_daemon_log(expression, delta=10):
    return _search_str_in_log_file(expression, DAEMON_LOG_INFO, delta)


def search_str_in_asterisk_log(expression, delta=10):
    return _search_str_in_log_file(expression, ASTERISK_LOG_INFO, delta)


def search_str_in_xivo_agent_log(expression, delta=10):
    return _search_str_in_log_file(expression, XIVO_AGENT_LOG_INFO, delta)


def _search_str_in_log_file(expression, loginfo, delta=10):
    command = ['tail', '-n', '15', loginfo.logfile]
    result = world.ssh_client_xivo.out_call(command)

    min_timestamp = datetime.now() - timedelta(seconds=delta)
    loglines = _get_lines_since_timestamp(result, min_timestamp, loginfo)

    for line in loglines:
        if expression in line:
            return True
    return False


def _get_lines_since_timestamp(text, min_timestamp, loginfo):
    lines = text.split("\n")
    date_match = re.compile(loginfo.date_pattern, re.I)

    res = []
    for line in lines:
        try:
            m = date_match.search(line)
            datetext = m.group(1)
        except (AttributeError, IndexError):
            continue
        timestamp = datetime.strptime(datetext, loginfo.date_format)
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
