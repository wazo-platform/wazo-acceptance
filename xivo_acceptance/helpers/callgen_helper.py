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

import socket

from subprocess import Popen, PIPE
from lettuce.registry import world
from xivo_lettuce import func


def killall_process_sipp():
    command = ['killall', 'sipp']
    _exec_cmd(command)


def execute_n_calls_then_hangup(count, extension, duration=3000, username='', password=''):
    number, context = func.extract_number_and_context_from_extension(extension)
    if not username or not password:
        callto_user = 'to_%s' % context
        callto_pass = 'to_%s' % context
    else:
        callto_user = username
        callto_pass = password

    command = ['xivo-callgen',
               '-bg',
               '-li', socket.gethostbyname(world.config.callgen_host),
               '-rh', world.config.xivo_host,
               'call-then-hangup',
               '-nc', count,
               '-ce', number,
               '-clu', callto_user,
               '-clp', callto_pass,
               '-cd', duration]
    _exec_cmd(command)


def execute_n_calls_then_wait(count, extension, username='', password=''):
    number, context = func.extract_number_and_context_from_extension(extension)
    if not username or not password:
        callto_user = 'to_%s' % context
        callto_pass = 'to_%s' % context
    else:
        callto_user = username
        callto_pass = password

    command = ['xivo-callgen',
               '-bg',
               '-li', socket.gethostbyname(world.config.callgen_host),
               '-rh', world.config.xivo_host,
               'call-then-wait',
               '-nc', count,
               '-ce', number,
               '-clu', callto_user,
               '-clp', callto_pass]
    _exec_cmd(command)


def execute_sip_register(username, password, expires=120):
    command = ['xivo-callgen',
               '-bg',
               '-li', socket.gethostbyname(world.config.callgen_host),
               '-rh', world.config.xivo_host,
               'send-sip-register',
               '-u', username,
               '-p', password,
               '-e', expires]
    _exec_cmd(command)


def execute_answer_then_hangup(duration=5000, ring_time=2000):
    command = ['xivo-callgen',
               '-bg',
               '-li', socket.gethostbyname(world.config.callgen_host),
               '-rh', world.config.xivo_host,
               'answer-then-hangup',
               '-cd', duration,
               '-rt', ring_time]
    _exec_cmd(command)


def execute_answer_then_wait(ring_time=2000):
    command = ['xivo-callgen',
               '-bg',
               '-li', socket.gethostbyname(world.config.callgen_host),
               '-rh', world.config.xivo_host,
               'answer-then-wait',
               '-rt', ring_time]
    _exec_cmd(command)


def execute_pickup_call(number, username, password):
    command = ['xivo-callgen',
               '-li', socket.gethostbyname(world.config.callgen_host),
               '-rh', world.config.xivo_host,
               'call-then-hangup',
               '-ce', number,
               '-clu', username,
               '-clp', password,
               '-cd', 5000]
    return _exec_cmd(command, ['-tt'])


def _exec_cmd(command, extra_ssh_args=None):
    cmds = []
    for arg in command:
        arg = '"' + str(arg) + '"'
        arg.encode('utf8')
        cmds.append(arg)

    ssh_command = ['ssh',
                   '-o', 'PreferredAuthentications=publickey',
                   '-o', 'StrictHostKeyChecking=no',
                   '-o', 'UserKnownHostsFile=/dev/null',
                   '-l', world.config.callgen_login]
    if extra_ssh_args:
        ssh_command.extend(extra_ssh_args)
    ssh_command.append(socket.gethostbyname(world.config.callgen_host))
    ssh_command.extend(cmds)

    p = Popen(ssh_command,
              stdout=PIPE,
              stderr=PIPE,
              close_fds=True)
    output = p.communicate()[0]

    if p.returncode != 0 and p.returncode != 99:
        print output

    return p.returncode
