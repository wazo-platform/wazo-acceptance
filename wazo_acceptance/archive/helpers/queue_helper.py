# -*- coding: utf-8 -*-
# Copyright 2013-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from lettuce import world

from xivo_acceptance.lettuce import sysutils


def add_queue(data):
    queue = {
        'name': data['name'].lower().strip(),
        'label': data['name'],
        'options': []
    }

    if 'maxlen' in data:
        queue['options'].append(['maxlen', data['maxlen']])
    if 'joinempty' in data:
        queue['options'].append(['joinempty', data['joinempty']])
    if 'leavewhenempty' in data:
        queue['options'].append(['leavewhenempty', data['leavewhenempty']])
    if 'ringing_time' in data:
        queue['timeout'] = data['ringing_time']
    if 'wrapuptime' in data:
        queue['options'].append(['wrapuptime', data['wrapuptime']])
    if 'reachability_timeout' in data:
        queue['options'].append(['timeout', data['reachability_timeout']])
    if 'ring_strategy' in data:
        queue['options'].append(['strategy', data['ring_strategy']])

    queue = world.confd_client.queues.create(queue)
    extension = {'exten': data['number'], 'context': data['context']}
    extension = world.confd_client.extensions.create(extension)
    world.confd_client.queues(queue).add_extension(extension)

    for agent_id in data.get('agents', []):
        world.confd_client.queues(queue).add_agent_member({'id': agent_id})
    for user_id in data.get('users', []):
        world.confd_client.queues(queue).add_user_member({'id': user_id})
    if 'schedule_id' in data:
        world.confd_client.queues(queue).add_schedule({'id': data['schedule_id']})


def add_or_replace_queue(queue_data):
    delete_queues_with_number(queue_data['number'])
    delete_queues_with_name(queue_data['name'])

    add_queue(queue_data)


def delete_queues_with_name_or_number(queue_name, queue_number):
    delete_queues_with_name(queue_name)
    delete_queues_with_number(queue_number)


def delete_queues_with_name(name):
    queues = world.confd_client.queues.list(name=name)['items']
    for queue in queues:
        world.confd_client.queues.delete(queue)
        if queue['extensions']:
            world.confd_client.extensions.delete(queue['extensions'][0])


def delete_queues_with_number(number):
    extensions = world.confd_client.extensions.list(exten=number, recurse=True)
    for extension in extensions['items']:
        if extension['queue']:
            world.confd_client.queues.delete(extension['queue']['id'])
        if extension['incall']:
            world.confd_client.incalls.delete(extension['incall']['id'])
        for line in extension['lines']:
            world.confd_client.lines.delete(line['id'])
        world.confd_client.extensions.delete(extension['id'])


def get_queue_by(**kwargs):
    queue = _find_queue_by(**kwargs)
    if not queue:
        raise Exception('Queue Not Found: %s' % kwargs)
    return queue


def _find_queue_by(name):
    queues = world.confd_client.queues.list(name=name)['items']
    for queue in queues:
        return queue
