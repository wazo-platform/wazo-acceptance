# -*- coding: utf-8 -*-

import os
import subprocess
import socket
from lettuce import before, after, world


def run_xivoclient():
    xc_path = os.environ['XC_PATH'] + '/'
    environment_variables = os.environ
    environment_variables['LD_LIBRARY_PATH'] = '.'
    world.xc_process = subprocess.Popen('./xivoclient',
                                        cwd=xc_path,
                                        env=environment_variables)


def xivoclient_step(f):
    """Decorator that sends the function name to the XiVO Client."""
    def xivoclient_decorator(step, *kargs):
        world.xc_socket.send('%s,%s\n' % (f.__name__, ','.join(kargs)))
        world.xc_response = str(world.xc_socket.recv(1024))
        print 'XC response: %s %r' % (f.__name__, world.xc_response)
        f(step, *kargs)
    return xivoclient_decorator


def xivoclient(f):
    """Decorator that sends the function name to the XiVO Client."""
    def xivoclient_decorator(*kargs):
        world.xc_socket.send('%s,%s\n' % (f.__name__, ','.join(kargs)))
        world.xc_response = str(world.xc_socket.recv(1024))
        print 'XC response: %s %r' % (f.__name__, world.xc_response)
        f(*kargs)
    return xivoclient_decorator


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
