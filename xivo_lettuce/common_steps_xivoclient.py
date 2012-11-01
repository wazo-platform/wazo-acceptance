# -*- coding: utf-8 -*-

import time
from lettuce import step, world
from xivo_lettuce.xivoclient import xivoclient, xivoclient_step
from xivo_lettuce.xivoclient import run_xivoclient, i_stop_the_xivo_client
from xivo_lettuce import common


@step(u'When I start the XiVO Client')
def i_start_the_xivo_client(step):
    run_xivoclient()

    # Waiting for the listening socket to open
    time.sleep(1)

    try:
        world.xc_socket.connect('/tmp/xivoclient')
    except:
        world.xc_process.terminate()
        raise


@step(u'I log in the XiVO Client as "([^"]*)", pass "([^"]*)"$')
def i_log_in_the_xivo_client_as_1_pass_2(step, login, password):
    xivo_address = common.get_host_address()
    i_log_in_the_xivo_client_to_host_1_as_2_pass_3(xivo_address,
                                                   login,
                                                   password)
    assert world.xc_response == 'OK'


@step(u'I log in the XiVO Client as "([^"]*)", pass "([^"]*)", unlogged agent$')
def i_log_in_the_xivo_client_as_1_pass_2_unlogged_agent(step, login, password):
    xivo_address = common.get_host_address()
    i_log_in_the_xivo_client_to_host_1_as_2_pass_3_unlogged_agent(xivo_address,
                                                                  login,
                                                                  password)
    assert world.xc_response == 'OK'


@step(u'I can\'t log in the XiVO Client as "([^"]*)", pass "([^"]*)"$')
def i_cant_log_in_the_xivo_client_as_1_pass_2(step, login, password):
    xivo_address = common.get_host_address()
    i_log_in_the_xivo_client_to_host_1_as_2_pass_3(xivo_address,
                                                   login,
                                                   password)
    assert world.xc_response != 'OK'


@xivoclient
def i_log_in_the_xivo_client_to_host_1_as_2_pass_3(host, login, password):
    time.sleep(world.xc_login_timeout)


@xivoclient
def i_log_in_the_xivo_client_to_host_1_as_2_pass_3_unlogged_agent(host, login, password):
    time.sleep(world.xc_login_timeout)


@step(u'I log out of the XiVO Client$')
@xivoclient_step
def i_log_out_of_the_xivo_client(step):
    assert world.xc_response == 'OK'
