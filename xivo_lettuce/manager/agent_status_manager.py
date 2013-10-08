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

from xivo_acceptance.helpers import line_helper, agent_helper, callgen_helper
from xivo_lettuce import sysutils


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
