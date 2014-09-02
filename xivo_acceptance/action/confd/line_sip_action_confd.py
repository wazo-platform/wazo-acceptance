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

LINES_SIP_URL = 'lines_sip'


def all_lines():
    return world.confd_utils_1_1.rest_get(LINES_SIP_URL)


def get(lineid):
    return world.confd_utils_1_1.rest_get('%s/%s' % (LINES_SIP_URL, lineid))


def create_line_sip(parameters):
    return world.confd_utils_1_1.rest_post(LINES_SIP_URL, parameters)


def update(lineid, parameters):
    return world.confd_utils_1_1.rest_put('%s/%s' % (LINES_SIP_URL, lineid), parameters)


def delete(line_id):
    return world.confd_utils_1_1.rest_delete('%s/%s' % (LINES_SIP_URL, line_id))
