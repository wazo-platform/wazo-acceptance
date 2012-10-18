# -*- coding: utf-8 -*-

from lettuce.registry import world
from xivo_ws.objects.queue import Queue


def get_queue_id_with_queue_name(queue_name):
    queues = world.ws.queues.list()
    for queue in queues:
        if queue.name == str(queue_name):
            return queue.id
    raise Exception('no queue with queue name %s' % queue_name)


def get_queue_id_with_number(queue_number):
    queues = world.ws.queues.search(queue_number)
    for queue in queues:
        if queue.number == str(queue_number):
            return queue.id
    raise Exception('no queue with queue number %s' % queue_number)


def delete_queue_with_name_if_exists(queue_displayname):
    try:
        queue_id = get_queue_id_with_queue_name(queue_displayname)
    except Exception:
        pass
    else:
        world.ws.queues.delete(queue_id)


def delete_queue_with_number_if_exists(queue_number):
    try:
        queue_id = get_queue_id_with_number(queue_number)
    except Exception:
        pass
    else:
        world.ws.queues.delete(queue_id)


def find_queue_id_with_displayname(queue_displayname):
    queues = world.ws.queues.search(queue_displayname)
    if queues:
        return [queue.id for queue in queues]
    return []


def find_queue_id_with_number(queue_number):
    queues = world.ws.queues.search(queue_number)
    if queues:
        return [queue.id for queue in queues]
    return []


def add_queue(data):
    queue = Queue()
    queue.name = data['name'].lower()
    queue.display_name = data['name']
    queue.number = data['number']
    queue.context = data['context']
    if 'maxlen' in data:
        queue.maxlen = data['maxlen']
    if 'agents' in data:
        queue.agents = data['agents']
    if 'joinempty' in data:
        queue.joinempty = data['joinempty']
    if 'leavewhenempty' in data:
        queue.leavewhenempty = data['leavewhenempty']
    if 'waittime' in data:
        queue.waittime = data['waittime']
    if 'waitratio' in data:
        queue.waitratio = data['waitratio']
    if 'schedule_id' in data:
        queue.schedule_id = data['schedule_id']
    if 'ringing_time' in data:
        queue.ringing_time = int(data['ringing_time'])
    world.ws.queues.add(queue)


def add_or_replace_queue(queue_data):
    queue_number = queue_data['number']
    delete_queue_with_number_if_exists(queue_number)

    add_queue(queue_data)
