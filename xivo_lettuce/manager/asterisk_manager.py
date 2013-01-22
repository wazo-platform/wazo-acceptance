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

from lettuce.registry import world


def get_asterisk_conf(file_name, var_name):
    command = ['xivo-confgen', 'asterisk/%s' % file_name, '|', 'grep', '-m', '1', var_name]
    ret = world.ssh_client_xivo.out_call(command)
    if ret:
        val = ret.split('=')[1].strip()
        return val
    assert(False)


def logoff_agents(agent_numbers):
    for agent_number in agent_numbers:
        logoff_agent(agent_number)


def logoff_agent(agent_number):
    asterisk_command = 'agent logoff Agent/%s' % (agent_number)
    send_to_asterisk_cli(asterisk_command)


def send_to_asterisk_cli(asterisk_command):
    check_output_asterisk_cli(asterisk_command)


def check_output_asterisk_cli(asterisk_command):
    shell_command = ['asterisk', '-rx', '"%s"' % asterisk_command]
    output = world.ssh_client_xivo.out_call(shell_command)
    return output
