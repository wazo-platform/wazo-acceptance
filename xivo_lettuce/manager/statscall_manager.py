# -*- coding: UTF-8 -*-

import socket

from subprocess import Popen, PIPE
from lettuce.registry import world
from utils.func import extract_number_and_context_from_extension


def killall_process_sipp():
    command = ['killall', 'sipp']
    _exec_cmd(command)


def execute_n_calls_then_hangup(count, extension, duration=3000, username='', password=''):
    number, context = extract_number_and_context_from_extension(extension)
    if not username or not password:
        callto_user = 'to_%s' % context
        callto_pass = 'to_%s' % context
    else:
        callto_user = username
        callto_pass = password

    command = ['xivo-callgen',
               '-bg',
               '-li', socket.gethostbyname(world.callgen_host),
               '-rh', world.xivo_host,
               'call-then-hangup',
               '-nc', count,
               '-ce', number,
               '-clu', callto_user,
               '-clp', callto_pass,
               '-cd', duration]
    _exec_cmd(command)


def execute_n_calls_then_wait(count, extension, username='', password=''):
    number, context = extract_number_and_context_from_extension(extension)
    if not username or not password:
        callto_user = 'to_%s' % context
        callto_pass = 'to_%s' % context
    else:
        callto_user = username
        callto_pass = password

    command = ['xivo-callgen',
               '-bg',
               '-li', socket.gethostbyname(world.callgen_host),
               '-rh', world.xivo_host,
               'call-then-wait',
               '-nc', count,
               '-ce', number,
               '-clu', callto_user,
               '-clp', callto_pass]
    _exec_cmd(command)


def execute_sip_register(username, password, expires=120):
    command = ['xivo-callgen',
               '-bg',
               '-li', socket.gethostbyname(world.callgen_host),
               '-rh', world.xivo_host,
               'send-sip-register',
               '-u', username,
               '-p', password,
               '-e', expires]
    _exec_cmd(command)


def execute_answer_then_hangup(duration=5000, ring_time=2000):
    command = ['xivo-callgen',
               '-bg',
               '-li', socket.gethostbyname(world.callgen_host),
               '-rh', world.xivo_host,
               'answer-then-hangup',
               '-cd', duration,
               '-rt', ring_time]
    _exec_cmd(command)


def execute_answer_then_wait(ring_time=2000):
    command = ['xivo-callgen',
               '-bg',
               '-li', socket.gethostbyname(world.callgen_host),
               '-rh', world.xivo_host,
               'answer-then-wait',
               '-rt', ring_time]
    _exec_cmd(command)


def execute_pickup_call(number, username, password):
    command = ['xivo-callgen',
               '-li', socket.gethostbyname(world.callgen_host),
               '-rh', world.xivo_host,
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
                   '-l', world.callgen_login]
    if extra_ssh_args:
        ssh_command.extend(extra_ssh_args)
    ssh_command.append(socket.gethostbyname(world.callgen_host))
    ssh_command.extend(cmds)

    p = Popen(ssh_command,
              stdout=PIPE,
              stderr=PIPE,
              close_fds=True)
    output = p.communicate()[0]

    if p.returncode != 0:
        print output

    return p.returncode
