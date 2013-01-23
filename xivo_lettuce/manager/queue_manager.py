# -*- coding: utf-8 -*-

# Copyright (C) 2013 Avencall
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

from xivo_lettuce.manager_ws import queue_manager_ws, context_manager_ws
from xivo_lettuce import form, sysutils
from xivo_lettuce.common import open_url, go_to_tab


def remove_queues_with_name_or_number_if_exist(queue_name, queue_number):
    queue_manager_ws.delete_queues_with_name(queue_name)
    queue_manager_ws.delete_queues_with_number(queue_number)


def type_queue_name_display_name_number_context(name, display_name, extension, context):
    form.input.set_text_field_with_label('Name', name)
    form.input.set_text_field_with_label('Display name', display_name)
    form.input.set_text_field_with_label('Number', extension)
    context = context_manager_ws.get_context_with_name(context)
    context_field_value = '%s (%s)' % (context.display_name, context.name)
    form.select.set_select_field_with_label('Context', context_field_value)


def type_queue_ring_strategy(ring_strategy):
    form.select.set_select_field_with_label('Ring strategy', ring_strategy)


def add_or_replace_queue(queue):
    open_url('queue', 'add')
    remove_queues_with_name_or_number_if_exist(queue['name'], queue['number'])
    type_queue_name_display_name_number_context(queue['name'], queue['display name'],
                                                queue['number'], queue['context'])
    if 'agents' in queue:
        _add_agents_to_queue(queue['agents'])

    form.submit.submit_form()


def _add_agents_to_queue(agents):
    go_to_tab('Members')
    pane = form.list_pane.ListPane.from_id('agentlist')
    for agent in agents.split(","):
        pane.add_contains(agent)


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

    queue_details = lines.pop(0).strip()
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


def does_queue_exist_in_asterisk(queue_name):
    output = _asterisk_queue_show(queue_name)
    return not output.startswith("No such queue")
