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
from xivo_lettuce import postgres
from xivo_lettuce import sysutils
from xivo_lettuce.manager import call_manager
from xivo_lettuce.manager_ws import line_manager_ws, agent_manager_ws


def log_agent_on_user(agent_number):
    line = _get_line_from_agent(agent_number)
    log_agent(agent_number, line.number)


def unlog_agent_from_user(agent_number):
    line = _get_line_from_agent(agent_number)
    unlog_agent(agent_number, line.number)


def log_agent(agent_number, extension):
    line = line_manager_ws.find_line_with_extension(extension)
    call_manager.execute_sip_register(line.name, line.secret)
    call_manager.execute_n_calls_then_wait(1, '*31%s' % agent_number, username=line.name, password=line.secret)
    world.logged_agents.append(agent_number)
    time.sleep(5)


def unlog_agent(agent_number, extension):
    line = line_manager_ws.find_line_with_extension(extension)
    call_manager.execute_n_calls_then_wait(1, '*32%s' % agent_number, username=line.name, password=line.secret)
    time.sleep(5)


def unlog_all_agents():
    sysutils.send_command(['xivo-agentctl', '-c', '"logoff all"'])


def _get_line_from_agent(agent_number):
    agent = agent_manager_ws.get_agent_with_number(agent_number)
    if not agent.users:
        raise Exception('agent %s has no users' % agent_number)
    user_id = agent.users[0]
    line = line_manager_ws.find_line_with_user_id(user_id)
    return line
