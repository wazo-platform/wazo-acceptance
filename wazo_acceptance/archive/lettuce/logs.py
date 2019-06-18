# -*- coding: utf-8 -*-
# Copyright 2013-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from collections import namedtuple
from datetime import datetime, timedelta
import re

from xivo_acceptance.lettuce import sysutils

WAZO_AGENTD_LOGFILE = '/var/log/wazo-agentd.log'

PYTHON_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
PYTHON_DATE_PATTERN = r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})"

LogfileInfo = namedtuple('LogfileInfo', ['logfile', 'date_format', 'date_pattern'])

WAZO_AGENTD_LOG_INFO = LogfileInfo(logfile=WAZO_AGENTD_LOGFILE,
                                   date_format=PYTHON_DATE_FORMAT,
                                   date_pattern=PYTHON_DATE_PATTERN)


def search_str_in_wazo_agentd_log(expression, delta=10):
    return _search_str_in_log_file(expression, WAZO_AGENTD_LOG_INFO, delta)


def _search_str_in_log_file(expression, loginfo, delta=10):
    loglines = _find_line_in_log_file(loginfo, delta)

    for line in loglines:
        if expression in line:
            return True
    return False


def _find_line_in_log_file(loginfo, delta=10):
    min_datetime = sysutils.xivo_current_datetime() - timedelta(seconds=delta)
    loglines = get_lines_since_timestamp(min_datetime, loginfo)
    return loglines


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


def _find_all_lines_in_log_file(loginfo):
    command = ['tail', '-n', '30', loginfo.logfile]
    result = sysutils.output_command(command)
    lines = result.split("\n")
    return lines


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
