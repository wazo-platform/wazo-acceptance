# -*- coding: utf-8 -*-

# Copyright (C) 2015 Avencall
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

import hashlib
import socket
import json
import threading
import time
import select

from collections import defaultdict
from Queue import Queue

from lettuce.decorators import step


@step(u'Given I connect to xivo-ctid and register the following commands:')
def given_i_connect_to_xivo_ctid_and_register_the_following_commands(step):
    listened_events = [line['event'] for line in step.hashes]
    step.scenario._pseudo_xivo_client = _new_client(listened_events)


@step(u'Given I send a "([^"]*)" for "([^"]*)" "([^"]*)"')
def given_i_send_a_command_for_uuid_id(step, command, uuid, id_):
    step.scenario._pseudo_xivo_client.register_user_status_update(uuid, id_)


@step(u'Then I should receive a "([^"]*)" with info:')
def then_i_should_receive_a_group1_with_info(step, cti_event):
    timeout = 10
    events = []
    to_match = len(step.hashes)

    while timeout and to_match > 0:
        events = step.scenario._pseudo_xivo_client.get_events(cti_event)
        for line in step.hashes:
            if 'user_id' in line:
                line['user_id'] = int(line['user_id'])

            matches = [event for event in events if event['data'] == line]
            to_match -= len(matches)
            if to_match <= 0:
                return
        time.sleep(1)
        timeout -= 1

    raise AssertionError('No matching event in %s for %s' % (events, step.hashes))


def _new_client(listened_events):

    class _Client(object):

        expected_events = listened_events

        def __init__(self, host, port, username, password):
            self._host = host
            self._port = port
            self._username = username
            self._password = password
            self._socket = None
            self._thread = None
            self._events_lock = threading.Lock()
            self._events = defaultdict(list)
            self._stop = False
            self._login_complete = False
            self._message_queue = Queue()

        def get_events(self, event_name):
            with self._events_lock:
                return self._events[event_name]

        def stop(self):
            self._stop = True
            if self._thread:
                self._thread.join()

        def connect(self):
            self._thread = threading.Thread(group=None, target=self._start)
            self._thread.start()

        def _queue_message(self, msg):
            while True:
                if self._login_complete:
                    break

            self._message_queue.put(msg)

        def _empty_msg_queue(self):
            while not self._message_queue.empty():
                msg = self._message_queue.get()
                self._send_message(msg)

        def _start(self):
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._socket.connect((self._host, self._port))
            self._send_login()
            self._recv()

        def _recv(self):
            data = ''
            while not self._stop:
                ready = select.select([self._socket], [], [], 0.1)
                if ready[0]:
                    data += self._socket.recv(4096)
                    while '\n' in data:
                        line, data = data.split('\n', 1)
                        message = json.loads(line)
                        self._on_message(message)
                        data = data.lstrip()
                self._empty_msg_queue()

        def _on_message(self, message):
            klass = message[u'class']
            fn_name = u'_on_{}'.format(klass)
            if hasattr(self, fn_name):
                getattr(self, fn_name)(message)
            elif klass in self.expected_events:
                with self._events_lock:
                    self._events[klass].append(message)

        def _send_message(self, message):
            msg = json.dumps(message)
            self._socket.sendall('{}\n'.format(msg))

        def register_user_status_update(self, uuid, user_id):
            msg = {
                'class': 'register_user_status_update',
                'user_ids': [(uuid, int(user_id))],
            }
            self._queue_message(msg)

        def _send_login(self):
            login_message = {
                'class': 'login_id',
                'userlogin': self._username,
                'company': 'lol',
                'ident': 'python-client',
                'xivoversion': '1.2',
                'version': '9999',
            }
            self._send_message(login_message)

        def _send_login_pass(self, sessionid):
            hashedpassword = hashlib.sha1('{}:{}'.format(sessionid, self._password)).hexdigest()
            login_pass_message = {
                "hashedpassword": hashedpassword,
                "class": "login_pass",
            }
            self._send_message(login_pass_message)

        def _send_login_capas(self, capaid):
            login_capas_message = {
                "loginkind": "user",
                "capaid": capaid,
                "lastconnwins": False,
                "state": "available",
                "class": "login_capas"
            }
            self._send_message(login_capas_message)

        def _on_login_id(self, message):
            self._send_login_pass(message['sessionid'])

        def _on_login_pass(self, message):
            self._send_login_capas(message['capalist'][0])
            self._login_complete = True

    c = _Client('10.37.1.254', 5003, 'alice', u'alice')
    c.connect()

    return c
