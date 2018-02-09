# -*- coding: utf-8 -*-
# Copyright (C) 2013-2015 Avencall
# Copyright (C) 2016 Proformatique Inc.
# SPDX-License-Identifier: GPL-3.0+

import time

from lettuce import world
from xivo_ws import Agent

from xivo_acceptance.helpers import user_helper
from xivo_acceptance.lettuce import func
from xivo_agentd_client.error import AgentdClientError


def add_agent(data_dict):
    agent = Agent()
    agent.firstname = data_dict['firstname']
    agent.number = data_dict['number']
    agent.context = data_dict['context']

    if 'lastname' in data_dict:
        agent.lastname = data_dict['lastname']
    if 'passwd' in data_dict:
        agent.passwd = data_dict['passwd']
    if 'users' in data_dict:
        agent.users = data_dict['users']

    world.ws.agents.add(agent)
    agent = _find_agent_with_number(data_dict['number'])
    return int(agent.id)


def delete_agents_with_number(number):
    for agent in _search_agents_with_number(number):
        world.ws.agents.delete(agent.id)


def find_agent_id_with_number(number):
    agent = _find_agent_with_number(number)
    return agent.id


def find_agent_password_with_number(number):
    agent = _find_agent_with_number(number)
    return agent.password


def get_agent_with_number(number):
    agent = _find_agent_with_number(number)
    return world.ws.agents.view(agent.id)


def _find_agent_with_number(number):
    return world.ws.agents.find_one_by_number(number)


def _search_agents_with_number(number):
    return world.ws.agents.search_by_number(number)


def login_agent(agent_number, extension=None, ignore_error=False):
    if extension is None:
        number, context = _get_extension_from_agent(agent_number)
    else:
        number, context = func.extract_number_and_context_from_extension(extension)
    try:
        world.agentd_client.agents.login_agent_by_number(agent_number, number, context)
    except AgentdClientError:
        if not ignore_error:
            raise


def logoff_agent(agent_number, ignore_error=False):
    try:
        world.agentd_client.agents.logoff_agent_by_number(agent_number)
    except AgentdClientError:
        if not ignore_error:
            raise


def login_agent_from_phone(agent_number, phone_register):
    number, context = _get_extension_from_agent(agent_number)
    user = user_helper.get_by_exten_context(number, context)
    fullname = " ".join([user['firstname'], user.get('lastname', '')])
    phone = phone_register.get_user_phone(fullname)
    phone.call('*31%s' % agent_number)
    time.sleep(3)


def logoff_agent_from_phone(agent_number, phone_register):
    number, context = _get_extension_from_agent(agent_number)
    user = user_helper.get_by_exten_context(number, context)
    fullname = " ".join([user['firstname'], user.get('lastname', '')])
    phone = phone_register.get_user_phone(fullname)
    phone.call('*32%s' % agent_number)
    time.sleep(3)


def is_agent_logged(agent_number):
    agent_status = world.agentd_client.agents.get_agent_status_by_number(agent_number)
    return agent_status.logged


def unlog_all_agents():
    world.agentd_client.agents.logoff_all_agents()


def pause_agent(agent_number):
    world.agentd_client.agents.pause_agent_by_number(agent_number)


def unpause_agent(agent_number):
    world.agentd_client.agents.unpause_agent_by_number(agent_number)


def _get_extension_from_agent(agent_number):
    agent = get_agent_with_number(agent_number)
    if not agent.users:
        raise Exception('agent %s has no users' % agent_number)
    user_id = agent.users[0]
    user = world.confd_client.users.get(user_id)
    extension = user['lines'][0]['extensions'][0]
    return extension['exten'], extension['context']
