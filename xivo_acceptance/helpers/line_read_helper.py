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


def find_by_id(line_id):
    try:
        return get_by_id(line_id)
    except HTTPError:
        return None


def get_by_id(line_id):
    return world.confd_client.lines.get(line_id)


def find_with_exten_context(exten, context='default'):
    extensions = world.confd_client.extensions.list(exten=exten, context=context)['items']
    if not extensions or not extensions[0]['lines']:
        return None

    line_id = extensions[0]['lines'][0]['id']
    return world.confd_client.lines.get(line_id)


def get_with_exten_context(exten, context='default'):
    line = find_with_exten_context(exten, context)
    assert_that(line, is_not(none()),
                "line with extension %s@%s not found" % (exten, context))
    return line


def find_line_id_with_exten_context(exten, context='default'):
    line = find_with_exten_context(exten, context)
    return line['id'] if line else None


def get_line_id_with_exten_context(exten, context='default'):
    line_id = find_line_id_with_exten_context(exten, context)
    assert_that(line_id, is_not(none()),
                "line with extension %s@%s not found" % (exten, context))
    return line_id


def find_extension_id_for_line(line_id):
    try:
        return get_extension_id_for_line(line_id)
    except IndexError:
        return None


def get_extension_id_for_line(line_id):
    response = world.confd_client.lines(line_id).list_extensions()
    return response['items'][0]['extension_id']
