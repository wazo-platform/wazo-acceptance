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

import time

from lettuce import world
from xivo_ws import Agent

from xivo_acceptance.helpers import line_helper, agent_helper, callgen_helper
from xivo_lettuce import sysutils


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


def log_agent_on_user(agent_number):
    line = _get_line_from_agent(agent_number)
    log_agent(agent_number, line.number)


def unlog_agent_from_user(agent_number):
    line = _get_line_from_agent(agent_number)
    unlog_agent(agent_number, line.number)


def log_agent(agent_number, extension):
    line = line_helper.find_with_extension(extension)
    callgen_helper.execute_sip_register(line.name, line.secret)
    callgen_helper.execute_n_calls_then_wait(1, '*31%s' % agent_number, username=line.name, password=line.secret)
    world.logged_agents.append(agent_number)
    time.sleep(5)


def unlog_agent(agent_number, extension):
    line = line_helper.find_with_extension(extension)
    callgen_helper.execute_n_calls_then_wait(1, '*32%s' % agent_number, username=line.name, password=line.secret)
    time.sleep(5)


def is_agent_logged_in(agent_number):
    command = ['xivo-agentctl', '-c', '"status %s"' % agent_number]
    output = sysutils.output_command(command)

    log_line = output.split("\n")[1]
    log_status = log_line.split(": ")[1].strip()

    return log_status == "True"


def unlog_all_agents():
    sysutils.send_command(['xivo-agentctl', '-c', '"logoff all"'])


def pause_agent(agent_number):
    command = ['xivo-agentctl', '-c', '"pause %s"' % agent_number]
    sysutils.send_command(command)


def unpause_agent(agent_number):
    command = ['xivo-agentctl', '-c', '"unpause %s"' % agent_number]
    sysutils.send_command(command)


def _get_line_from_agent(agent_number):
    agent = agent_helper.get_agent_with_number(agent_number)
    if not agent.users:
        raise Exception('agent %s has no users' % agent_number)
    user_id = agent.users[0]
    line = line_helper.find_with_user_id(user_id)
    return line