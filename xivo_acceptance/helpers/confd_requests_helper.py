# -*- coding: utf-8 -*-
# Copyright (C) 2013-2014 Avencall
# SPDX-License-Identifier: GPL-3.0+

import re
from urlparse import urlparse

from xivo_acceptance.lettuce import logs

DATE_PATTERN = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d+)\s*'
PID_PATTERN = r'\[([0-9]+)\]\s*'
LOG_LVL_PATTERN = r'\(([A-Z]+)\)\s*'
FILE_LOGGER_PATTERN = r'\(([a-z\._]+)\):\s*'
HTTP_METHOD_PATTERN = r'([A-Z]+)\s*'
URL_PATTERN = r'([\w\:\./_\?\&\%=\-]+)\s*'
DATA_PATTERN = r'(?:with data (.*))?'


def last_requests_infos():
    extracted = logs.find_line_in_xivo_confd_log(delta=20)
    raw_list = [_extract_request_infos(log_line) for log_line in extracted]

    return [log_line for log_line in raw_list if log_line is not None]


def _extract_request_infos(request):
    s_pat_list = [
        DATE_PATTERN,
        PID_PATTERN,
        LOG_LVL_PATTERN,
        FILE_LOGGER_PATTERN,
        HTTP_METHOD_PATTERN,
        URL_PATTERN,
        DATA_PATTERN
    ]
    s_pat = r'^%s' % ''.join(s_pat_list)

    pat = re.compile(s_pat)
    m = re.match(pat, request)

    if m is None:
        return None

    date, pid, log_lvl, file_logger, method, url, data = m.groups()

    url_obj = urlparse(url)

    res = {}
    res['date'] = date
    res['pid'] = pid
    res['log_lvl'] = log_lvl
    res['file_logger'] = file_logger
    res['method'] = method
    res['scheme'] = url_obj.scheme
    res['port'] = url_obj.port
    res['path'] = url_obj.path
    res['params'] = url_obj.params
    res['query'] = url_obj.query
    res['hostname'] = url_obj.hostname
    res['data'] = data.strip() if data else ''

    return res
