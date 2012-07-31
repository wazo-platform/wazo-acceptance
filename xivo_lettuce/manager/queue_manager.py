# -*- coding: utf-8 -*-

import json
from xivo_lettuce.common import get_webservices

WSQ = get_webservices('queue')


def delete_queue_from_displayname(queue_displayname):
    for id in find_queue_id_from_displayname(queue_displayname):
        WSQ.delete(id)


def find_queue_id_from_displayname(queue_displayname):
    queue_list = WSQ.list()
    if queue_list:
        return [queueinfo['id'] for queueinfo in queue_list if
                queueinfo['displayname'] == queue_displayname]
    return []


def delete_queue_from_number(queue_number):
    for id in find_queue_id_from_number(queue_number):
        WSQ.delete(id)


def find_queue_id_from_number(queue_number):
    queue_list = WSQ.list()
    if queue_list:
        return [queueinfo['id'] for queueinfo in queue_list if
                queueinfo['number'] == queue_number]
    return []


def insert_queue(data):
    jsoncontent = WSQ.get_json_file_content('queue')
    datajson = jsoncontent % {
                              'name': data['name'],
                              'number': data['number'],
                              'context': data['context'],
                              'maxlen': data['maxlen'],
                              'agents': data['agents']
                             }
    data = json.loads(datajson)
    WSQ.add(data)
