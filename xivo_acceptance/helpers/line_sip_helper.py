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

from hamcrest import assert_that, equal_to, is_not, none

from xivo_acceptance.action.confd import line_sip_action_confd as line_sip_action
from xivo_lettuce.remote_py_cmd import remote_exec


def create_line_sip(parameters):
    remote_exec(_create_line_sip, parameters=parameters)


def _create_line_sip(channel, parameters):
    from xivo_dao.data_handler.line import services as line_services
    from xivo_dao.data_handler.line.model import LineSIP

    line = LineSIP(**parameters)
    line_services.create(line)


def find_by_username(username):
    all_lines = _all_lines()
    found = [line for line in all_lines if line['username'] == username]
    return found[0] if found else None


def _all_lines():
    response = line_sip_action.all_lines()
    assert_that(response.status, equal_to(200), str(response.data))
    return response.data['items']


def get_by_username(username):
    line = find_by_username(username)
    assert_that(line, is_not(none()), "line with username '%s' does not exist" % username)
    return line
