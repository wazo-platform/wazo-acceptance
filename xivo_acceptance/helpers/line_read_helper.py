# -*- coding: utf-8 -*-

# Copyright (C) 2013-2016 Avencall
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

from lettuce import world

from hamcrest import assert_that
from hamcrest import is_not
from hamcrest import none
from requests.exceptions import HTTPError

from xivo_acceptance.lettuce import func
from xivo_acceptance.action.confd import line_extension_action_confd as line_extension_action
from xivo_acceptance.action.confd import line_action_confd as line_action


def find_by_id(line_id):
    response = line_action.get(line_id)
    return response.resource() if response.status_ok() else None


def get_by_id(line_id):
    line = find_by_id(line_id)
    assert_that(line, is_not(none()),
                "line with id %s not found" % line_id)
    return line


def find_with_exten_context(exten, context='default'):
    response = world.confd_client.extensions.list(exten=exten, context=context)
    if response['total'] < 1:
        return None
    extension_id = response['items'][0]['id']

    try:
        response = world.confd_client.extensions(extension_id).get_line()
    except HTTPError:
        return None

    line_id = response['line_id']

    return get_by_id(line_id)


def get_with_exten_context(exten, context='default'):
    line = find_with_exten_context(exten, context)
    assert_that(line, is_not(none()),
                "line with extension %s@%s not found" % (exten, context))
    return line


def find_with_extension(extension):
    number, context = func.extract_number_and_context_from_extension(extension)
    return find_with_exten_context(number, context)


def find_with_name(name):
    response = line_action.all_lines()
    found = [line for line in response.items()
             if line['name'] == name]
    return found[0] if found else None


def find_line_id_with_exten_context(exten, context='default'):
    line = find_with_exten_context(exten, context)
    return line['id'] if line else None


def get_line_id_with_exten_context(exten, context='default'):
    line_id = find_line_id_with_exten_context(exten, context)
    assert_that(line_id, is_not(none()),
                "line with extension %s@%s not found" % (exten, context))
    return line_id


def find_extension_id_for_line(line_id):
    response = line_extension_action.get(line_id)
    return response.resource()['extension_id'] if response.status_ok() else None


def get_extension_id_for_line(line_id):
    extension_id = find_extension_id_for_line(line_id)
    assert_that(extension_id, is_not(none()),
                "Line %s has no extension" % line_id)
    return extension_id
