# -*- coding: utf-8 -*-

from lettuce.registry import world


def delete_line_with_number(number, context):
    for id in find_line_id_with_number(number, context):
        world.ws.lines.delete(id)


def find_line_id_with_number(number, context):
    lines = world.ws.lines.search_by_number(number)
    if lines:
        return [line.id for line in lines if
                line.number == str(number) and line.context == str(context)]
    return []
