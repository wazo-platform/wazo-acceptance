# -*- coding: utf-8 -*-

# Copyright (C) 2013-2014 Avencall
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

from lettuce.registry import world


CALL_LOGS_URL = '/call_logs'
HEADERS = {'Accept': 'text/csv; charset=utf-8'}


def call_logs_list():
    return world.confd_utils_1_1.rest_get(CALL_LOGS_URL, headers=HEADERS)


def call_logs_list_interval(params):
    return world.confd_utils_1_1.rest_get(CALL_LOGS_URL,
                                          params=params,
                                          headers=HEADERS)
