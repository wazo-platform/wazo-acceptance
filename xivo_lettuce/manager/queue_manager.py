# -*- coding: utf-8 -*-

from lettuce.registry import world
from xivo_lettuce.common import *

WS = get_webservices('queue')


def delete_queue_from_displayname(queue_displayname):
    for id in find_queue_id_from_displayname(queue_displayname):
        WS.delete(id)


def find_queue_id_from_displayname(queue_displayname):
    queue_list = WS.list()
    if queue_list:
        return [queueinfo['id'] for queueinfo in queue_list if
                queueinfo['displayname'] == queue_displayname]
    return []


def delete_queue_from_number(queue_number):
    for id in find_queue_id_from_number(queue_number):
        WS.delete(id)


def find_queue_id_from_number(queue_number):
    queue_list = WS.list()
    if queue_list:
        return [queueinfo['id'] for queueinfo in queue_list if
                queueinfo['number'] == queue_number]
    return []
