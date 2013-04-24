# -*- coding: utf-8 -*-

# Copyright (C) 2013 Avencall
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

import os
import subprocess
import socket
import json
import time
import errno
from lettuce import before, after, world

DEBUG = False


@before.each_scenario
def setup_xivoclient_rc(scenario):
    world.xc_process = None


@after.each_scenario
def clean_xivoclient_rc(scenario):
    if world.xc_process:
        world.xc_process.poll()
        if world.xc_process.returncode is None:
            exec_command('i_stop_the_xivo_client')
        stop_xivoclient()


def start_xivoclient(argument=''):
    xc_path = os.environ['XC_PATH'] + '/'
    environment_variables = os.environ
    environment_variables['LD_LIBRARY_PATH'] = '.'
    try:
        world.xc_process = subprocess.Popen(['./xivoclient', argument],
                                            cwd=xc_path,
                                            env=environment_variables)
    except OSError as e:
        if e.errno == errno.ENOENT:
            raise Exception('XiVO Client executable not found')
        else:
            raise

    # Waiting for the listening socket to open
    time.sleep(1)

    world.xc_socket = socket.socket(socket.AF_UNIX)
    try:
        world.xc_socket.connect('/tmp/xivoclient')
    except socket.error as(error_number, message):
        if error_number == errno.ENOENT:
            raise Exception('XiVO Client must be built for functional testing')
        else:
            raise Exception(message)


def stop_xivoclient():
    if world.xc_process:
        world.xc_process.terminate()
        world.xc_socket.close()
        world.xc_process = None
        world.xc_socket = None


def exec_command(cmd, *kargs):
    formatted_command = _format_command(cmd, kargs)
    return _send_and_receive_command(formatted_command)


def _format_command(function_name, arguments):
    command = {'function_name': function_name,
               'arguments': arguments}
    formatted_command = json.dumps(command)
    return formatted_command


def _send_and_receive_command(formatted_command):
    if DEBUG:
        from pprint import pprint
        print '-------------------- MSG SEND ---------------------'
        pprint(formatted_command)
    world.xc_socket.send('%s\n' % formatted_command)
    response_raw = str(world.xc_socket.recv(1024))
    if DEBUG:
        print '------------------ RAW RESPONSE -------------------'
        pprint(response_raw)
    response_dict = json.loads(response_raw)
    if DEBUG:
        print '---------------- DECODED RESPONSE -----------------'
        pprint(response_dict)
        print '------------------ END RESPONSE -------------------'
        print
    return response_dict
