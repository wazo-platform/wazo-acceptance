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

from lettuce import world
from xivo_lettuce import func


def delete_lines_with_number(number, context):
    for line in _search_lines_with_number(number, context):
        world.ws.lines.delete(line.id)


def find_line_with_number(number, context):
    lines = _search_lines_with_number(number, context)
    if len(lines) != 1:
        raise Exception('expecting 1 line with number %r and context %r; found %s' %
                        (number, context, len(lines)))
    return lines[0]


def find_line_with_name(name):
    lines = _search_lines_with_name(name)
    if len(lines) != 1:
        raise Exception('expecting 1 line with name %r; found %s' %
                        (name, len(lines)))
    return lines[0]


def find_line_id_with_number(number, context):
    line = find_line_with_number(number, context)
    return line.id


def find_line_with_extension(extension):
    number, context = func.extract_number_and_context_from_extension(extension)
    return find_line_with_number(number, context)


def find_line_with_user_id(user_id):
    lines = _search_lines_with_user_id(user_id)
    if len(lines) != 1:
        raise Exception('expecting 1 line with user ID %r; found %s' %
                        (user_id, len(lines)))
    return lines[0]


def is_line_with_number_exists(number, context):
    lines = _search_lines_with_number(number, context)
    return bool(lines)


def _search_lines_with_user_id(user_id):
    user_id = int(user_id)
    lines = world.ws.lines.list()
    return [line for line in lines if line.user_id == user_id]


def _search_lines_with_number(number, context):
    context = str(context)
    lines = world.ws.lines.search_by_number(number)
    return [line for line in lines if line.context == context]


def _search_lines_with_name(name):
    return world.ws.lines.search_by_name(name)
