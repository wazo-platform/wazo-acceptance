# -*- coding: utf-8 -*-

import json
from xivo_lettuce.common import get_webservices
from lettuce.registry import world

WSQ = get_webservices('queue')


def get_queue_id_with_queue_name(queue_name):
    queues = world.ws.queues.search(queue_name)
    for queue in queues:
        if queue.name == str(queue_name):
            return queue.id
    raise Exception('no queue with queue name %s' % queue_name)


def delete_queue_with_displayname(queue_displayname):
    for id in find_queue_id_with_displayname(queue_displayname):
        WSQ.delete(id)


def delete_queue_with_number(queue_number):
    for id in find_queue_id_with_number(queue_number):
        WSQ.delete(id)


def find_queue_id_with_displayname(queue_displayname):
    queue_list = WSQ.list()
    if queue_list:
        return [queueinfo['id'] for queueinfo in queue_list if
                queueinfo['displayname'] == queue_displayname]
    return []


def find_queue_id_with_number(queue_number):
    queue_list = WSQ.list()
    if queue_list:
        return [queueinfo['id'] for queueinfo in queue_list if
                queueinfo['number'] == queue_number]
    return []


def add_queue(data):
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
