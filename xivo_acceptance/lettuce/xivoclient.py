# -*- coding: utf-8 -*-

# Copyright 2013-2017 The Wazo Authors  (see the AUTHORS file)
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

import errno
import json
import logging
import os
import pprint
import socket
import subprocess
import uuid

from lettuce import before, after, world
from xivo_acceptance.lettuce import common

logger = logging.getLogger('cticlient')


class XivoClient(object):

    environment_variables = os.environ
    environment_variables['LD_LIBRARY_PATH'] = '.'
    xc_path = os.environ['XC_PATH'] + '/'
    arguments = []
    socket = None
    process = None
    socket_dir = '/tmp'
    socket_name = ''
    socket_path = ''

    def __init__(self, argument='', name='default', debug=False):
        self.arguments.append(argument)
        uid = uuid.uuid4()
        self.socket_name = 'xc-%s-%s.sock' % (name, uid.hex)
        self.socket_path = os.path.join(self.socket_dir, self.socket_name)
        self.debug = debug

    def start(self):
        world.display.get_instance()
        self.launch()
        message = ('Error while connecting to the xivoclient socket: the socket {socket} does not exist. '
                   'The cause may be: XiVO Client multiples instance is disabled, or '
                   'the XiVO Client was not built for functional testing.').format(socket=self.socket_path)
        common.wait_until(self.listen_socket, tries=3, message=message)

    def is_running(self):
        return self.process is not None and self.process.poll() is None

    def stop(self):
        logger.debug('-------------------- STOP CLIENT ---------------------')
        if self.is_running():
            self.process.terminate()
            self.process = None
        if self.socket:
            self.socket.close()
            self.socket = None
        try:
            logger.debug('-------------------- REMOVE SOCKET %s ---------------------', self.socket_path)
            os.remove(self.socket_path)
        except OSError:
            pass

    def clean(self):
        if self.is_running():
            self.exec_command('i_stop_the_xivo_client')
        self.stop()

    def launch(self):
        logger.debug('-------------------- LAUNCHING CLIENT ---------------------')
        try:
            args = ['./wazoclient']
            args.extend(self.arguments)
            args.append('socket:%s' % self.socket_path)
            self.process = subprocess.Popen(args,
                                            cwd=self.xc_path,
                                            env=self.environment_variables)
        except OSError as e:
            if e.errno == errno.ENOENT:
                raise Exception('XiVO Client executable not found')
            else:
                raise

    def listen_socket(self):
        logger.debug('-------------------- LISTENING SOCKET: %s ---------------------', self.socket_path)
        if not self.is_running():
            raise Exception('XiVO Client has crashed')
        self.socket = socket.socket(socket.AF_UNIX)
        try:
            self.socket.connect(self.socket_path)
        except socket.error as(error_number, message):
            if error_number == errno.ENOENT:
                return False
            else:
                raise Exception(message)
        return True

    def exec_command(self, cmd, *kargs):
        if not self.is_running():
            raise Exception('XiVO Client is not running')
        formatted_command = self._format_command(cmd, kargs)
        return self._send_and_receive_command(formatted_command)

    def _format_command(self, function_name, arguments):
        command = {'function_name': function_name,
                   'arguments': arguments}
        formatted_command = json.dumps(command)
        return formatted_command

    def _send_and_receive_command(self, formatted_command):
        self._send_command(formatted_command)
        response_raw = self._receive_command()
        response_decoded = self._decode_response(response_raw)
        return response_decoded

    def _send_command(self, formatted_command):
        logger.debug('-------------------- MSG SENT ---------------------')
        logger.debug(pprint.pformat(formatted_command))
        logger.debug('-------------------- END MSG ----------------------')
        self.socket.send('%s\n' % formatted_command)

    def _receive_command(self):
        socket_buffer = self.socket.makefile()
        response_raw = str(socket_buffer.readline())
        socket_buffer.close()
        logger.debug('------------------ RAW RESPONSE -------------------')
        logger.debug(pprint.pformat((response_raw)))
        logger.debug('------------------ END RESPONSE -------------------')
        return response_raw

    def _decode_response(self, response_raw):
        response_dict = json.loads(response_raw)
        logger.debug('---------------- DECODED RESPONSE -----------------')
        logger.debug(pprint.pformat(response_dict))
        logger.debug('------------------ END RESPONSE -------------------')
        return response_dict


@before.each_scenario
def setup_xivoclient_rc(scenario):
    world.xc_process_dict = {}
    world.xc_instance = None
    world.xc_result = None


@after.each_scenario
def clean_xivoclient_rc(scenario):
    for instance in world.xc_process_dict.itervalues():
        instance.clean()


def exec_command(cmd, *kargs):
    return world.xc_instance.exec_command(cmd, *kargs)


def start_xivoclient(argument='', name='default'):
    if name not in world.xc_process_dict:
        client_obj = XivoClient(argument, name=name)
        client_obj.start()
        _add_new_instance(name, client_obj)


def start_xivoclient_with_errors(argument='', name='default'):
    if name not in world.xc_process_dict:
        client_obj = XivoClient(argument, name=name)
        try:
            client_obj.start()
        except Exception:
            logger.info('got an expected error when starting xivo client')
            client_obj.clean()
        else:
            _add_new_instance(name, client_obj)


def stop_xivoclient(name='default'):
    if name in world.xc_process_dict:
        world.xc_process_dict[name].stop()
        del world.xc_process_dict[name]


def _add_new_instance(name, instance):
    world.xc_process_dict[name] = instance
    if name == 'default':
        world.xc_instance = instance
