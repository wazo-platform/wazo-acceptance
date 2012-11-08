# -*- coding: utf-8 -*-

from lettuce import world
from xivo_ws import Queue


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
    if 'users' in data:
        queue.users = data['users']
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
    if 'wrapuptime' in data:
        queue.wrapuptime = data['wrapuptime']
    world.ws.queues.add(queue)


def add_or_replace_queue(queue_data):
    queue_number = queue_data['number']
    delete_queues_with_number(queue_number)

    add_queue(queue_data)


def delete_queues_with_name(name):
    for queue in _search_queues_with_name(name):
        world.ws.queues.delete(queue.id)


def delete_queues_with_number(number):
    for queue in _search_queues_with_number(number):
        world.ws.queues.delete(queue.id)


def get_queue_with_name(name):
    queue = _find_queue_with_name(name)
    return world.ws.queues.view(queue.id)


def find_queue_id_with_name(name):
    queue = _find_queue_with_name(name)
    return queue.id


def _find_queue_with_name(name):
    queues = _search_queues_with_name(name)
    if len(queues) != 1:
        raise Exception('expecting 1 queue with name %r: found %s' %
                        (name, len(queues)))
    return queues[0]


def _find_queue_with_number(number):
    queues = _search_queues_with_number(number)
    if len(queues) != 1:
        raise Exception('expecting 1 queue with number %r: found %s' %
                        (number, len(queues)))
    return queues[0]


def _search_queues_with_name(name):
    # name is not the same as display name
    name = unicode(name)
    queues = world.ws.queues.list()
    return [queue for queue in queues if queue.name == name]


def _search_queues_with_number(number):
    number = unicode(number)
    queues = world.ws.queues.search(number)
    return [queue for queue in queues if queue.number == number]
