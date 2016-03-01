# -*- coding: utf-8 -*-

# Copyright (C) 2015-2016 Avencall
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
import json
import threading
import time
import select

from hamcrest import assert_that
from hamcrest import is_
from lettuce.registry import world
from Queue import Queue

from lettuce.decorators import step

from xivo_acceptance.helpers import (user_helper, xivo_helper)


@step(u'Given I connect to xivo-ctid:')
def given_i_connect_to_xivo_ctid(step):
    username, password = map(step.hashes[0].get, ['username', 'password'])
    c = step.scenario._pseudo_xivo_client = _Client(world.config['xivo_host'], 5003, username, password)
    c.connect()


@step(u'Given I send a cti message:')
def given_i_send_a_cti_message(step):
    msg = json.loads(step.multiline)
    step.scenario._pseudo_xivo_client.empty_event_queue()
    step.scenario._pseudo_xivo_client.send_message(msg)


@step(u'Then I should receive the following cti command:')
def then_i_should_receive_the_following_cti_command(step):
    events = step.scenario._pseudo_xivo_client.events
    assert_that(_has_received_event_before_timeout(events, step.multiline, 5),
                'CTI event {} was not received'.format(step.multiline))


@step(u'(?:Given|When) I send a SwitchboardHold message')
def when_i_send_switchboardhold_message(step):
    msg = {'class': 'hold_switchboard',
           'queue_name': '__switchboard_hold'}
    step.scenario._pseudo_xivo_client.send_message(msg)


@step(u'Then I should receive the following chat message:')
def then_i_should_receive_the_following_chat_message(step):
    data = step.hashes[0]
    local_xivo_uuid = xivo_helper.get_uuid()
    user_id = user_helper.get_by_firstname_lastname(data['firstname'], data['lastname'])['id']
    to = local_xivo_uuid, user_id
    expected_raw_event = {'class': 'chitchat',
                          'alias': data['alias'],
                          'to': to,
                          'from': json.loads(data['from']),
                          'text': data['msg']}
    events = step.scenario._pseudo_xivo_client.events
    assert_that(_has_received_event_before_timeout(events, json.dumps(expected_raw_event), 5),
                'CTI event {} was not received'.format(expected_raw_event))


@step(u'Then I should NOT receive the following cti command:')
def then_i_should_not_receive_the_following_cti_command(step):
    events = step.scenario._pseudo_xivo_client.events
    assert_that(_has_received_event_before_timeout(events, step.multiline, 5), is_(False),
                'Received an unexpected CTI event {}'.format(step.multiline))


def _has_received_event_before_timeout(events, expected_raw, timeout):
    expected_msg = json.loads(expected_raw)
    start_time = time.time()

    while time.time() - start_time < timeout:
        if events.empty():
            time.sleep(0.1)
            continue

        event = events.get()

        if event['class'] != expected_msg['class']:
            continue

        if _message_matches_ignore_timenow(event, expected_msg):
            return True

    return False


def _message_matches_ignore_timenow(msg, expected_msg):
    msg.pop('timenow', None)

    return expected_msg == msg


class _Client(object):

    LOGIN_TIMEOUT = 10

    def __init__(self, host, port, username, password):
        self._host = host
        self._port = port
        self._username = username
        self._password = password
        self._socket = None
        self._thread = None
        self.events = Queue()
        self._stop = False
        self._login_complete = threading.Event()

    def stop(self):
        self._stop = True
        if self._thread:
            self._thread.join()

    def connect(self):
        self._thread = threading.Thread(target=self._start)
        self._thread.start()

    def send_message(self, msg):
        if not self._login_complete.wait(self.LOGIN_TIMEOUT):
            raise Exception('could not send message: client is not logged')

        self._send_message(msg)

    def empty_event_queue(self):
        while not self.events.empty():
            self.events.get()

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

    def _on_message(self, message):
        klass = message[u'class']
        fn_name = u'_on_{}'.format(klass)
        if hasattr(self, fn_name):
            getattr(self, fn_name)(message)
        else:
            self.events.put(message)

    def _send_message(self, message):
        msg = json.dumps(message)
        self._socket.sendall('{}\n'.format(msg.rstrip()))

    def _send_login(self):
        login_message = {
            'class': 'login_id',
            'userlogin': self._username,
            'company': 'lol',
            'ident': 'python-client',
            'xivoversion': '2.0',
        }
        self._send_message(login_message)

    def _send_login_pass(self, sessionid):
        login_pass_message = {
            "password": self._password,
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
        self._login_complete.set()
