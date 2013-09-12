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

import re
from urlparse import urlparse

from hamcrest import assert_that, is_not, none
from xivo_lettuce import sysutils, logs

DATE_PATTERN = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d+)\s*'
PID_PATTERN = r'xivo-restapid\[([0-9]+)\]\s*'
LOG_LVL_PATTERN = r'\(([A-Z]+)\)\s*'
FILE_LOGGER_PATTERN = r'\(([a-z\._]+)\):\s*'
HTTP_METHOD_PATTERN = r'([A-Z]+)\s*'
URL_PATTERN = r'([\w\:\./_\?\&\%=\-]+)\s*'
DATA_PATTERN = r'(?:with data (.*))?'


def assert_last_request_matches(**expected_request_infos):
    last_request = _get_last_request()
    request_infos = _extract_request_infos(last_request)

    for request_info_key, request_info_value in expected_request_infos.iteritems():
        try:
            result = re.match(request_info_value, request_infos[request_info_key])
        except TypeError:
            result = request_info_value == request_infos[request_info_key]
        assert_that(result, is_not(none()), '%s != %s' % (request_info_value, request_infos[request_info_key]))


def _get_last_request():
    last_line = sysutils.output_command(['tail', '-n', '1', logs.XIVO_RESTAPI_LOGFILE])
    return last_line


def _extract_request_infos(request):
    s_pat_list = [DATE_PATTERN, PID_PATTERN, LOG_LVL_PATTERN, FILE_LOGGER_PATTERN, HTTP_METHOD_PATTERN, URL_PATTERN, DATA_PATTERN]
    s_pat = r'^%s' % ''.join(s_pat_list)

    pat = re.compile(s_pat)
    m = re.match(pat, request)
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
    res['data'] = data

    return res
