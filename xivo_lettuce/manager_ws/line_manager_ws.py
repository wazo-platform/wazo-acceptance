# -*- coding: utf-8 -*-

from lettuce import world


def delete_line_with_number(number, context):
    for line_id in find_line_id_with_number(number, context):
        world.ws.lines.delete(line_id)


def find_line_id_with_number(number, context):
    context = str(context)

    lines = world.ws.lines.search_by_number(number)
    return [line.id for line in lines if line.context == context]


def is_line_with_number_exists(number, context):
    context = str(context)

    lines = world.ws.lines.search_by_number(number)
    for line in lines:
        if line.context == context:
            return True
    return False
