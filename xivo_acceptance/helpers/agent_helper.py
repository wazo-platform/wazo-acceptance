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
from xivo_ws import Agent

from xivo_acceptance.helpers import line_helper


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


def add_or_replace_agent(data_dict):
    agent_number = data_dict['number']
    delete_agents_with_number(agent_number)

    return add_agent(data_dict)


def delete_agent_with_id(agent_id):
    world.ws.agents.delete(agent_id)


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


def is_agent_logged_in(agent_number):
    agent_status = world.agentd_client.agents.get_agent_status_by_number(agent_number)
    return agent_status.logged


def unlog_all_agents():
    world.agentd_client.agents.logoff_all()


def pause_agent(agent_number):
    world.agentd_client.agents.pause_agent_by_number(agent_number)


def unpause_agent(agent_number):
    world.agentd_client.agents.unpause_agent_by_number(agent_number)


def _get_line_from_agent(agent_number):
    agent = get_agent_with_number(agent_number)
    if not agent.users:
        raise Exception('agent %s has no users' % agent_number)
    user_id = agent.users[0]
    line = line_helper.find_with_user_id(user_id)
    return line
