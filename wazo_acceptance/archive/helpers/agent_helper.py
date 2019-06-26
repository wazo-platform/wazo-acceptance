# -*- coding: utf-8 -*-
# Copyright 2013-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import time

from lettuce import world

from xivo_acceptance.helpers import user_helper
from xivo_acceptance.lettuce import func
from wazo_agentd_client.error import AgentdClientError


def add_agent(data_dict):
    agent = world.confd_client.agents.create(data_dict)
    # When agent will be multi-tenant
    # entity_name = data_dict.pop('entity', None)
    # tenant_uuid = tenant_helper.get_tenant_uuid(entity_name)
    # agent = world.confd_client.agents.create(data_dict, tenant_uuid=tenant_uuid)

    for user_id in data_dict.get('users', []):
        world.confd_client.users(user_id).add_agent(agent['id'])

    return agent['id']


def delete_agents_with_number(number):
    agents = world.confd_client.agents.list(number=number)['items']
    for agent in agents:
        world.confd_client.agents.delete(agent['id'])


def find_agent_by(**kwargs):
    agents = world.confd_client.agents.list(**kwargs)['items']
    for agent in agents:
        return agent


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


def unlog_all_agents():
    world.agentd_client.agents.logoff_all_agents()


def pause_agent(agent_number):
    world.agentd_client.agents.pause_agent_by_number(agent_number)


def unpause_agent(agent_number):
    world.agentd_client.agents.unpause_agent_by_number(agent_number)


def _get_extension_from_agent(agent_number):
    agent = find_agent_by(number=agent_number)
    if not agent['users']:
        raise Exception('agent %s has no users' % agent_number)
    user = world.confd_client.users.get(agent['users'][0]['uuid'])
    extension = user['lines'][0]['extensions'][0]
    return extension['exten'], extension['context']
