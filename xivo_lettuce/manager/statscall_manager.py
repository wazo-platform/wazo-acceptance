# -*- coding: UTF-8 -*-

from subprocess import Popen, PIPE, STDOUT
from lettuce.registry import world
import socket


def execute_n_calls_then_hangup(count, number, username='to_statscenter', password='to_statscenter', duration=2000):
    command = ['xivo-callgen',
               '-bg',
               '-li', socket.gethostbyname(world.callgen_host),
               '-rh', world.xivo_host,
               'call-then-hangup',
               '-nc', count,
               '-ce', number,
               '-clu', username,
               '-clp', password,
               '-cd', duration]
    _exec_cmd(command)


def execute_n_calls_then_wait(count, number, username='to_statscenter', password='to_statscenter'):
    command = ['xivo-callgen',
               '-bg',
               '-li', socket.gethostbyname(world.callgen_host),
               '-rh', world.xivo_host,
               'call-then-wait',
               '-nc', count,
               '-ce', number,
               '-clu', username,
               '-clp', password]
    _exec_cmd(command)


def execute_sip_register(username, password, expires=120):
    command = ['xivo-callgen',
               '-bg',
               '-rh', world.xivo_host,
               'send-sip-register',
               '-u', username,
               '-p', password,
               '-e', expires]
    _exec_cmd(command)


def execute_answer_then_hangup(duration=5000):
    command = ['xivo-callgen',
               '-bg',
               '-rh', world.xivo_host,
               'answer-then-hangup',
               '-cd', duration]
    _exec_cmd(command)


def execute_answer_then_wait(duration=10000):
    command = ['xivo-callgen',
               '-bg',
               '-rh', world.xivo_host,
               'answer-then-wait',
               '-cd', duration]
    _exec_cmd(command)


def _exec_cmd(command):
    cmds = []
    for arg in command:
        arg = str(arg)
        arg.encode('utf8')
        cmds.append(arg)

    ssh_command = ['ssh',
                   '-o', 'PreferredAuthentications=publickey',
                   '-o', 'StrictHostKeyChecking=no',
                   '-o', 'UserKnownHostsFile=/dev/null',
                   '-l', 'root',
                   '192.168.32.229']
    ssh_command.extend(cmds)

    p = Popen(ssh_command,
              stdout=PIPE,
              stderr=STDOUT,
              close_fds=True)
    output = p.communicate()[0]

    if p.returncode != 0:
        print output

    return output
