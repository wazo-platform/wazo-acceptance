# -*- coding: utf-8 -*-

import time
from lettuce import step, world
from xivo_lettuce.xivoclient import xivoclient, xivoclient_step
from xivo_lettuce.xivoclient import run_xivoclient
from xivo_lettuce import common
from xivo_lettuce.manager_ws import user_manager_ws


@step(u'When I start the XiVO Client')
def i_start_the_xivo_client(step):
    run_xivoclient()

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


@step(u'When I disable access to XiVO Client to user "([^"]*)" "([^"]*)"')
def when_i_disable_access_to_xivo_client_to_user_group1_group2(step, firstname, lastname):
    user_manager_ws.disable_cti_client(firstname, lastname)


@step(u'When I enable access to XiVO Client to user "([^"]*)" "([^"]*)"')
def when_i_enable_access_to_xivo_client_to_user_group1_group2(step, firstname, lastname):
    user_manager_ws.enable_cti_client(firstname, lastname)


@step(u'Then I can\'t connect the CTI client of "([^"]*)" "([^"]*)"')
def then_i_can_t_connect_the_cti_client_of_group1_group2(step, firstname, lastname):
    _log_user_in_client(firstname, lastname)
    assert world.xc_response != 'OK'


@step(u'Then I can connect the CTI client of "([^"]*)" "([^"]*)"')
def then_i_can_connect_the_cti_client_of_group1_group2(step, firstname, lastname):
    _log_user_in_client(firstname, lastname)
    assert world.xc_response == 'OK'


def _log_user_in_client(firstname, lastname):
    xivo_address = common.get_host_address()
    user = user_manager_ws.find_user_with_firstname_lastname(firstname, lastname)
    login = user.client_username
    password = user.client_password
    i_log_in_the_xivo_client_to_host_1_as_2_pass_3(xivo_address,
                                                   login,
                                                   password)
