# -*- coding: utf-8 -*-

# Copyright (C) 2013-2014 Avencall
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

from lettuce import world

from xivo_ws import Queue
from xivo_lettuce import sysutils
from xivo_lettuce.postgres import exec_sql_request


def add_queue(data):
    queue = Queue()
    queue.name = data['name'].lower().strip()
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
        queue.ringing_time = data['ringing_time']
    if 'wrapuptime' in data:
        queue.wrapuptime = data['wrapuptime']
    world.ws.queues.add(queue)


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


def find_queue_with_id(queue_id):
    return world.ws.queues.view(queue_id)


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


def set_penalty_for_agent(queue_name, agent_id, penalty):
    query = 'UPDATE queuemember SET penalty = :penalty WHERE queue_name = :queue_name AND userid = :userid AND usertype = \'agent\''
    exec_sql_request(query, queue_name=queue_name, userid=agent_id, penalty=penalty)


def delete_queue_with_id(queue_id):
    try:
        find_queue_with_id(queue_id)
    except ValueError:
        return
    world.ws.queues.delete(queue_id)


def get_penalty_for_agent(queue_name, agent_id):
    query = 'SELECT penalty FROM queuemember WHERE queue_name = :queue_name AND userid = :userid AND usertype = \'agent\''
    return exec_sql_request(query, queue_name=queue_name, userid=agent_id).first()['penalty']

def get_queue_member(queue_name, agent_id):
    query = 'SELECT * FROM queuemember WHERE queue_name = :queue_name AND userid = :userid AND usertype = \'agent\''
    row = exec_sql_request(query, queue_name=queue_name, userid=agent_id).first()
    return row
