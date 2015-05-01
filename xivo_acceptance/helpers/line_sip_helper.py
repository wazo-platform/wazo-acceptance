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

from hamcrest import assert_that, is_not, none

from xivo_acceptance.action.confd import line_sip_action_confd as line_sip_action


def find_by_username(username):
    response = line_sip_action.all_lines()
    found = [line for line in response.items()
             if line['username'] == username]
    return found[0] if found else None


def get_by_username(username):
    line = find_by_username(username)
    assert_that(line, is_not(none()),
                "line with username '%s' does not exist" % username)
    return line


def get_by_id(line_id):
    response = line_sip_action.get(line_id)
    return response.resource()


def delete_line(line_id):
    response = line_sip_action.delete(line_id)
    response.check_status()


def create_line(parameters):
    response = line_sip_action.create_line_sip(parameters)
    return response.resource()
