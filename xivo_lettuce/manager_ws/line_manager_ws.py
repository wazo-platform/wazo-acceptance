# -*- coding: utf-8 -*-

from lettuce import world
from utils.func import extract_number_and_context_from_extension


def delete_line_with_number(number, context):
    for line in _search_lines_with_number(number, context):
        world.ws.lines.delete(line.id)


def is_line_with_number_exists(number, context):
    lines = _search_lines_with_number(number, context)
    return bool(lines)


def find_line_with_number(number, context):
    lines = _search_lines_with_number(number, context)
    if len(lines) != 1:
        raise Exception('expecting 1 line with number %r and context %r; found %s' %
                        (number, context, len(lines)))
    return lines[0]


def find_line_with_extension(extension):
    number, context = extract_number_and_context_from_extension(extension)
    return find_line_with_number(number, context)


def find_line_with_user(user_id):
    lines = world.ws.lines.list()
    for line in lines:
        if line.user_id == user_id:
            return line


def find_line_id_with_number(number, context):
    line = find_line_with_number(number, context)
    return line.id


def _search_lines_with_number(number, context):
    context = str(context)

    lines = world.ws.lines.search_by_number(number)
    return [line for line in lines if line.context == context]
