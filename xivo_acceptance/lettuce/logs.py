# -*- coding: utf-8 -*-
# Copyright 2013-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from collections import namedtuple
from datetime import datetime, timedelta
import re

from xivo_acceptance.lettuce import sysutils


DAEMON_LOGFILE = '/var/log/daemon.log'
ASTERISK_LOGFILE = '/var/log/asterisk/messages'
XIVO_AGENT_LOGFILE = '/var/log/xivo-agentd.log'

DAEMON_DATE_FORMAT = "%b %d %H:%M:%S"
DAEMON_DATE_PATTERN = r"([\w]{3} [\d ]{2} [\d]{2}:[\d]{2}:[\d]{2})"

PYTHON_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
PYTHON_DATE_PATTERN = r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})"

LogfileInfo = namedtuple('LogfileInfo', ['logfile', 'date_format', 'date_pattern'])

DAEMON_LOG_INFO = LogfileInfo(logfile=DAEMON_LOGFILE,
                              date_format=DAEMON_DATE_FORMAT,
                              date_pattern=DAEMON_DATE_PATTERN)

ASTERISK_LOG_INFO = LogfileInfo(logfile=ASTERISK_LOGFILE,
                                date_format=DAEMON_DATE_FORMAT,
                                date_pattern=DAEMON_DATE_PATTERN)

XIVO_AGENT_LOG_INFO = LogfileInfo(logfile=XIVO_AGENT_LOGFILE,
                                  date_format=PYTHON_DATE_FORMAT,
                                  date_pattern=PYTHON_DATE_PATTERN)


def search_str_in_asterisk_log(expression, delta=10):
    return _search_str_in_log_file(expression, ASTERISK_LOG_INFO, delta)


def search_str_in_xivo_agent_log(expression, delta=10):
    return _search_str_in_log_file(expression, XIVO_AGENT_LOG_INFO, delta)


def _find_line_in_log_file(loginfo, delta=10):
    min_datetime = sysutils.xivo_current_datetime() - timedelta(seconds=delta)
    loglines = get_lines_since_timestamp(min_datetime, loginfo)
    return loglines


def _find_all_lines_in_log_file(loginfo):
    command = ['tail', '-n', '30', loginfo.logfile]
    result = sysutils.output_command(command)
    lines = result.split("\n")
    return lines


def _search_str_in_log_file(expression, loginfo, delta=10):
    loglines = _find_line_in_log_file(loginfo, delta)

    for line in loglines:
        if expression in line:
            return True
    return False


def get_lines_since_timestamp(min_timestamp, loginfo):
    lines = _find_all_lines_in_log_file(loginfo)
    date_re = re.compile(loginfo.date_pattern, re.I)
    after_date = False

    res = []
    for line in lines:
        if after_date:
            res.append(line)
            continue

        date_match = date_re.search(line)
        if not date_match:
            continue

        datetext = date_match.group(1)
        timestamp = datetime.strptime(datetext, loginfo.date_format)
        timestamp = _add_year_to_datetime(timestamp)
        if timestamp >= min_timestamp:
            res.append(line)
            after_date = True

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
