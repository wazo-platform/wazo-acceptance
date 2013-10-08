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

from xivo_acceptance.helpers import context_helper
from xivo_lettuce import sysutils
from xivo_lettuce.common import open_url, go_to_tab
from xivo_lettuce.form.input import set_text_field_with_label
from xivo_lettuce.form.select import set_select_field_with_label, \
    set_select_field_with_id
from xivo_lettuce.form.checkbox import set_checkbox_with_id
from xivo_lettuce.form.list_pane import ListPane
from xivo_lettuce.form.submit import submit_form
from xivo_lettuce.manager_ws import queue_manager_ws


CALLEE_TRANSFER = 'allow allee transfer'
CALLER_HANGUP = 'allow caller hangup'
REACH_TIMEOUT = 'member reachability timeout'
CALL_RETRY = 'call retry time'
REASSIGN_DELAY = 'reassign delay'
AUTOPAUSE_AGENTS = 'autopause agents'


def remove_queues_with_name_or_number(queue_name, queue_number):
    queue_manager_ws.delete_queues_with_name(queue_name)
    queue_manager_ws.delete_queues_with_number(queue_number)


def type_queue_ring_strategy(ring_strategy):
    set_select_field_with_label('Ring strategy', ring_strategy)


def add_or_replace_queue(queue):
    remove_queues_with_name_or_number(queue['name'], queue['number'])
    open_url('queue', 'add')
    fill_form(queue)


def add_or_replace_switchboard_queue(name, number, context, agents):
    config = {
        'name': name,
        'display name': name,
        'number': number,
        'context': context,
        'agents': agents,
        CALLEE_TRANSFER: 'true',
        CALLER_HANGUP: 'true',
        REACH_TIMEOUT: 'Disabled',
        CALL_RETRY: '1 second',
        REASSIGN_DELAY: 'Disabled',
        AUTOPAUSE_AGENTS: 'false',
    }

    add_or_replace_queue(config)
    submit_form()


def add_or_replace_switchboard_hold_queue(name, number, context):
    config = {
        'name': name,
        'display name': name,
        'number': number,
        'context': context,
    }

    add_or_replace_queue(config)
    submit_form()


def fill_form(queue):
    fill_general_tab(queue)
    fill_application_tab(queue)
    fill_advanced_tab(queue)

    if 'agents' in queue:
        agentlist = queue['agents'].split(",")
        add_agents_to_queue(agentlist)


def fill_general_tab(queue):
    go_to_tab('General')

    set_text_field_with_label('Name', queue['name'])
    set_text_field_with_label('Display name', queue['display name'])
    set_text_field_with_label('Number', queue['number'])

    context = context_helper.get_context_with_name(queue['context'])
    context_field_value = '%s (%s)' % (context.display_name, context.name)
    set_select_field_with_label('Context', context_field_value)

    if 'ring strategy' in queue:
        type_queue_ring_strategy(queue['ring strategy'])


def fill_application_tab(queue):
    go_to_tab('Application')

    if CALLEE_TRANSFER in queue:
        callee_transfer = (queue[CALLEE_TRANSFER] == 'true')
        set_checkbox_with_id('it-queuefeatures-hitting-callee', callee_transfer)

    if CALLER_HANGUP in queue:
        caller_hangup = (queue[CALLER_HANGUP] == 'true')
        set_checkbox_with_id('it-queuefeatures-hitting-caller', caller_hangup)


def fill_advanced_tab(queue):
    go_to_tab('Advanced')

    if REACH_TIMEOUT in queue:
        set_select_field_with_id('it-queue-timeout',
                                 queue[REACH_TIMEOUT])

    if CALL_RETRY in queue:
        set_select_field_with_id('it-queue-retry', queue[CALL_RETRY])

    if REASSIGN_DELAY in queue:
        set_select_field_with_id('it-queue-wrapuptime', queue[REASSIGN_DELAY])

    if AUTOPAUSE_AGENTS in queue:
        autopause_agents = (queue[AUTOPAUSE_AGENTS] == 'true')
        set_checkbox_with_id('it-queue-autopause', autopause_agents)


def add_agents_to_queue(agents):
    go_to_tab('Members')
    pane = ListPane.from_id('agentlist')
    for agent in agents:
        pane.add_contains(agent)


def remove_agents_from_queue(agents):
    go_to_tab('Members')
    pane = ListPane.from_id('agentlist')
    for agent in agents:
        pane.remove_contains(agent)


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


def does_queue_exist_in_asterisk(queue_name):
    output = _asterisk_queue_show(queue_name)
    return not output.startswith("No such queue")
