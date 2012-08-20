# -*- coding: UTF-8 -*-

from subprocess import Popen, PIPE, STDOUT
from lettuce.registry import world
import socket


def execute_n_calls_to(count, number, username='to_statscenter', password='to_statscenter', close='hangup', duration=2000):
    command = ['xivo-callgen',
               '-bg',
               '-li', socket.gethostbyname(world.jenkins_hostname),
               '-rh', world.remote_host,
               'call-then-%s' % close,
               '-nc', count,
               '-ce', number,
               '-clu', username,
               '-clp', password,
               '-cd', duration]
    _exec_cmd(command)


def execute_sip_register(username, password, expires=120):
    command = ['xivo-callgen',
               '-bg',
               '-rh', world.remote_host,
               'send-sip-register',
               '-u', username,
               '-p', password,
               '-e', expires]
    _exec_cmd(command)


def execute_answer_then_hangup(duration=5000):
    command = ['xivo-callgen',
               '-bg',
               '-rh', world.remote_host,
               'answer-then-hangup',
               '-cd', duration]
    _exec_cmd(command)


def _exec_cmd(command):
    cmds = []
    for arg in command:
        arg = str(arg)
        arg.encode('utf8')
        cmds.append(arg)

    p = Popen(cmds,
              stdout=PIPE,
              stderr=STDOUT,
              close_fds=True)
    output = p.communicate()[0]

    if p.returncode != 0:
        print output

    return output
