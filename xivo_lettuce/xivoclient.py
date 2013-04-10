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


def run_xivoclient():
    xc_path = os.environ['XC_PATH'] + '/'
    environment_variables = os.environ
    environment_variables['LD_LIBRARY_PATH'] = '.'
    try:
        world.xc_process = subprocess.Popen('./xivoclient',
                                            cwd=xc_path,
                                            env=environment_variables)
    except OSError as e:
        if e.errno == errno.ENOENT:
            raise Exception('XiVO Client executable not found')
        else:
            raise

    # Waiting for the listening socket to open
    time.sleep(1)


def xivoclient_step(f):
    """Decorator that sends the function name to the XiVO Client."""
    def xivoclient_decorator(step, *kargs):
        formatted_command = _format_command(f.__name__, kargs)
        _send_and_receive_command(formatted_command)
        print 'XC response: %s %r' % (f.__name__, world.xc_response)
        f(step, *kargs)
    return xivoclient_decorator


def xivoclient(f):
    """Decorator that sends the function name to the XiVO Client."""
    def xivoclient_decorator(*kargs):
        formatted_command = _format_command(f.__name__, kargs)
        _send_and_receive_command(formatted_command)
        print 'XC response: %s %r' % (f.__name__, world.xc_response)
        f(*kargs)
    return xivoclient_decorator


def _format_command(function_name, arguments):
    command = {'function_name': function_name,
               'arguments': arguments}
    formatted_command = json.dumps(command)
    return formatted_command


def _send_and_receive_command(formatted_command):
    world.xc_socket.send('%s\n' % formatted_command)
    response_json = str(world.xc_socket.recv(1024))
    response_dict = json.loads(response_json)
    from pprint import pprint
    pprint(response_dict)
    world.xc_response = response_dict['test_result']


@before.each_scenario
def setup_xivoclient_rc(scenario):
    world.xc_process = None
    world.xc_socket = socket.socket(socket.AF_UNIX)


@after.each_scenario
def clean_xivoclient_rc(scenario):
    if world.xc_process:
        world.xc_process.poll()
        if world.xc_process.returncode is None:
            i_stop_the_xivo_client()


@xivoclient
def i_stop_the_xivo_client():
    assert world.xc_response == "OK"
