# -*- coding: utf-8 -*-

from lettuce.registry import world
from xivo_ws.objects.queue import Queue


def get_queue_id_with_queue_name(queue_name):
    queues = world.ws.queues.search(queue_name)
    for queue in queues:
        if queue.name == str(queue_name):
            return queue.id
    raise Exception('no queue with queue name %s' % queue_name)


def get_queue_id_with_number(queue_number):
    queues = world.ws.queues.search(queue_number)
    for queue in queues:
        if queue.name == str(queue_number):
            return queue.id
    raise Exception('no queue with queue number %s' % queue_number)


def delete_queue_with_displayname(queue_displayname):
    try:
        world.ws.queues.delete(get_queue_id_with_queue_name(queue_displayname))
    except Exception:
        pass


def delete_queue_with_number(queue_number):
    try:
        world.ws.queues.delete(get_queue_id_with_number(queue_number))
    except Exception:
        pass


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
    queue.name = data['name']
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
    world.ws.queues.add(queue)
