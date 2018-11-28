# -*- coding: utf-8 -*-
# Copyright 2013-2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from lettuce import world

from xivo_acceptance.lettuce import sysutils
from . import extension_helper


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
    extension_helper.add_or_replace_extension(extension)

    for agent_id in data.get('agents', []):
        world.confd_client.queues(queue).add_agent_member({'id': agent_id})
    for user_id in data.get('users', []):
        world.confd_client.queues(queue).add_agent_member({'id': user_id})
    if 'schedule_id' in data:
        world.confd_client.queues(queue).add_schedule({'id': data['schedule_id']})


def add_or_replace_queue(queue_data):
    queue_name = queue_data['name']
    queue_number = queue_data['number']
    delete_queues_with_number(queue_number)
    delete_queues_with_name(queue_name)

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
    extension = extension_helper.find_extension_by_exten_context(number)
    world.confd_client.extensions.delete(extension)
    if extension['queue']:
        world.confd_client.queues.delete(extension['queue']['uuid'])


def get_queue_by(**kwargs):
    queue = find_queue_by(**kwargs)
    if not queue:
        raise Exception('Queue Not Found: %s' % kwargs)
    return queue


def find_queue_by(name):
    queues = world.confd_client.queues.list(name=name)['items']
    for queue in queues:
        return queue


def does_queue_exist_in_asterisk(queue_name):
    output = _asterisk_queue_show(queue_name)
    return not output.startswith("No such queue")


def agent_numbers_from_asterisk(queue_name):
    output = _asterisk_queue_show(queue_name)
    agent_numbers = _parse_members(output)
    return agent_numbers


def _asterisk_queue_show(queue_name):
    command = ['asterisk', '-rx', '"queue show %s"' % queue_name]
    output = sysutils.output_command(command)
    return output


def _parse_members(output):
    lines = output.split("\n")

    lines.pop(0).strip()
    member_header = lines.pop(0).strip()

    if member_header == "No Members":
        return []

    agent_numbers = []
    while lines[0].strip() not in ['Callers:', 'No Callers']:
        line = lines.pop(0).strip()
        agent_number = _parse_member_line(line)
        agent_numbers.append(agent_number)

    return agent_numbers


def _parse_member_line(member_line):
    agent, _, _ = member_line.partition(" ")
    membertype, number = agent.split("/")
    if membertype != "Agent":
        raise Exception("membertype %s different from Agent" % membertype)
    return int(number)
