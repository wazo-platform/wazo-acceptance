# -*- coding: utf-8 -*-
# Copyright (C) 2014 Avencall
# SPDX-License-Identifier: GPL-3.0-or-later

import jinja2
import select
import socket
from lettuce import world


def do_simultaneous_requests(n, agi_name, agi_args):
    connections = [_AGIConnection() for _ in xrange(n)]
    test = _AGISimultaneousTest(connections)
    test.prepare()
    test.execute(agi_name, agi_args)


class _AGIConnection(object):

    _PORT = 4573

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def close(self):
        self.sock.close()

    def connect(self):
        self.sock.connect((world.config['xivo_host'], self._PORT))

    def recv(self):
        data = self.sock.recv(2048)
        return data

    def send(self, data):
        self.sock.send(data)


class _AGISimultaneousTest(object):

    _TEMPLATE = jinja2.Template('''\
agi_network: yes
agi_network_script: {{ agi_name }}
agi_request: agi://127.0.0.1/{{ agi_name }}
agi_channel: SIP/je5qtq-00000067
agi_language: fr_FR
agi_type: SIP
agi_uniqueid: 1407844711.104
agi_version: 11.11.0
agi_callerid: 1001
agi_calleridname: Foo Bar
agi_callingpres: 0
agi_callingani2: 0
agi_callington: 0
agi_callingtns: 0
agi_dnid: 16
agi_rdnis: unknown
agi_context: default
agi_extension: 16
agi_priority: 2
agi_enhanced: 0.0
agi_accountcode: 
agi_threadid: -1254360208
{% for agi_arg in agi_args -%}
agi_arg_{{ loop.index }}: {{ agi_arg }}
{% endfor %}

''')

    def __init__(self, connections):
        self.connections = connections

    def prepare(self):
        for conn in self.connections:
            conn.connect()
            conn.sock.setblocking(0)

    def execute(self, agi_name, agi_args):
        data = self._TEMPLATE.render(agi_name=agi_name, agi_args=agi_args)
        fd_to_conn = {}
        poller = select.poll()

        for conn in self.connections:
            fd = conn.sock.fileno()
            fd_to_conn[fd] = conn
            poller.register(fd, select.POLLIN)

        for conn in self.connections:
            # we suppose that the remote TCP window is large enough so that the call send() won't
            # raise an EWOULDBLOCK error
            conn.send(data)

        while fd_to_conn:
            ready = poller.poll()
            for fd, mode in ready:
                conn = fd_to_conn[fd]
                if mode & select.POLLIN:
                    data = conn.recv()
                    if data:
                        conn.send('200 result=1\n')
                    else:
                        conn.close()
                        del fd_to_conn[fd]
                        poller.unregister(fd)
                else:
                    conn.close()
                    del fd_to_conn[fd]
                    poller.unregister(fd)
