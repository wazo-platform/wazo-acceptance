# -*- coding: utf-8 -*-

from lettuce.registry import world
from xivo_lettuce.common import *

WS = get_webservices('line')


def delete_line_from_number(line_number):
    for id in find_line_id_from_number(line_number):
        WS.delete(id)


def find_line_id_from_number(line_number):
    line_list = WS.list()
    if line_list:
        return [lineinfo['id'] for lineinfo in line_list if
                lineinfo['number'] == str(line_number)]
    return []
