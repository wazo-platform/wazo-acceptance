# -*- coding: utf-8 -*-
# Copyright 2013-2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from selenium.common.exceptions import ElementClickInterceptedException
from xivo_acceptance.helpers import context_helper, queue_helper
from xivo_acceptance.lettuce import common
from xivo_acceptance.action.webi import common as common_action_webi
from xivo_acceptance.lettuce.form.input import set_text_field_with_label
from xivo_acceptance.lettuce.form.select import set_select_field_with_label, \
    set_select_field_with_id
from xivo_acceptance.lettuce.form.checkbox import set_checkbox_with_id
from xivo_acceptance.lettuce.form.list_pane import ListPane
from xivo_acceptance.lettuce.form.submit import submit_form


CALLEE_TRANSFER = 'allow allee transfer'
CALLER_HANGUP = 'allow caller hangup'
REACH_TIMEOUT = 'member reachability timeout'
CALL_RETRY = 'call retry time'
REASSIGN_DELAY = 'reassign delay'
AUTOPAUSE_AGENTS = 'autopause agents'


def type_queue_ring_strategy(ring_strategy):
    try:
        set_select_field_with_label('Ring strategy', ring_strategy)
    except ElementClickInterceptedException:
        '''Sometimes, the list of extensions hides the field'''
        common_action_webi.reset_focus()
        set_select_field_with_label('Ring strategy', ring_strategy)


def type_queue_exit_context(context_name):
    set_text_field_with_label('Exit context', context_name)


def add_or_replace_queue(queue):
    queue_helper.delete_queues_with_name_or_number(queue['name'], queue['number'])
    common.open_url('queue', 'add')
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
        if isinstance(queue['agents'], list):
            agentlist = queue['agents']
        else:
            agentlist = queue['agents'].split(",")
        add_agents_to_queue(agentlist)


def fill_general_tab(queue):
    common.go_to_tab('General')

    set_text_field_with_label('Name', queue['name'])
    set_text_field_with_label('Display name', queue['display name'])

    context = context_helper.get_context_with_name(queue['context'])
    context_field_value = '%s (%s)' % (context.display_name, context.name)
    set_select_field_with_label('Context', context_field_value)

    if 'ring strategy' in queue:
        type_queue_ring_strategy(queue['ring strategy'])

    set_text_field_with_label('Number', queue['number'])


def fill_application_tab(queue):
    common.go_to_tab('Application')

    if CALLEE_TRANSFER in queue:
        callee_transfer = (queue[CALLEE_TRANSFER] == 'true')
        set_checkbox_with_id('it-queuefeatures-hitting-callee', callee_transfer)

    if CALLER_HANGUP in queue:
        caller_hangup = (queue[CALLER_HANGUP] == 'true')
        set_checkbox_with_id('it-queuefeatures-hitting-caller', caller_hangup)

    if 'timeout' in queue:
        set_text_field_with_label('Ringing time', queue['timeout'])


def fill_advanced_tab(queue):
    common.go_to_tab('Advanced')

    if REACH_TIMEOUT in queue:
        set_select_field_with_id('it-queue-timeout',
                                 queue[REACH_TIMEOUT])

    if CALL_RETRY in queue:
        set_select_field_with_id('it-queue-retry', queue[CALL_RETRY])

    if REASSIGN_DELAY in queue:
        set_select_field_with_id('it-queue-wrapuptime', queue[REASSIGN_DELAY])

    if AUTOPAUSE_AGENTS in queue:
        autopause_agents = 'Yes' if (queue[AUTOPAUSE_AGENTS] == 'true') else 'No'
        set_select_field_with_id('it-queue-autopause', autopause_agents)


def add_agents_to_queue(agents):
    common.go_to_tab('Members')
    pane = ListPane.from_id('agentlist')
    for agent in agents:
        pane.add_contains(agent)


def remove_agents_from_queue(agents):
    common.go_to_tab('Members')
    pane = ListPane.from_id('agentlist')
    for agent in agents:
        pane.remove_contains(agent)
