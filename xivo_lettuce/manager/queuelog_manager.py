# -*- coding: utf-8 -*-

from lettuce.registry import world
from subprocess import Popen, PIPE, STDOUT
import socket


def create_pgpass_on_remote_host():
    cmd = ['echo', '*:*:asterisk:asterisk:proformatique', '>', '.pgpass']
    world.ssh_client.check_call(cmd)
    cmd = ['chmod', '600', '.pgpass']
    world.ssh_client.check_call(cmd)


def delete_event_by_queue(event, queuename):
    create_pgpass_on_remote_host()
    pg_command = '"DELETE FROM queue_log WHERE queuename = \'%s\' and event = \'%s\'"' % (queuename, event)
    command = ['psql', '-h', 'localhost', '-U', 'asterisk', '-c', pg_command]
    world.ssh_client.check_call(command)


def get_event_count_queue(event, queuename):
    create_pgpass_on_remote_host()
    pg_command = '"SELECT COUNT(*) FROM queue_log WHERE queuename = \'%s\' and event = \'%s\'"' % (queuename, event)
    command = ['psql', '-h', 'localhost', '-U', 'asterisk', '-c', pg_command]
    res = world.ssh_client.out_call(command)
    return int(res.split('\n')[-4].strip())


def execute_call_event_full(count, queuename, number):
    command = ['xivo-callgen', 'queue_log_event',
               '-e', 'full',
               '-nb', count,
               '-rh', world.remote_host,
               '-li', socket.gethostbyname(world.jenkins_hostname),
               '-ce', number]
    _exec_cmd(command)


def execute_call_event_enterqueue(count, queuename, number):
    command = ['xivo-callgen', 'queue_log_event',
               '-e', 'enterqueue',
               '-nb', count,
               '-rh', world.remote_host,
               '-li', socket.gethostbyname(world.jenkins_hostname),
               '-ce', number]
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
