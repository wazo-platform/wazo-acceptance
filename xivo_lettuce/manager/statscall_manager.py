# -*- coding: UTF-8 -*-

from subprocess import Popen, PIPE, STDOUT
from lettuce.registry import world
import socket


def execute_n_calls_to(count, number):
    command = ['xivo-callgen',
               '-bg',
               '-li', socket.gethostbyname(world.jenkins_hostname),
               '-rh', world.remote_host,
               'call-then-hangup',
               '-nc', count,
               '-ce', number,
               '-clu', 'to_statscenter',
               '-clp', 'to_statscenter']
    _exec_cmd(command)


def _exec_cmd(command):
    p = Popen(command,
              stdout=PIPE,
              stderr=STDOUT,
              close_fds=True)
    output = p.communicate()[0]

    if p.returncode != 0:
        print output

    return output
