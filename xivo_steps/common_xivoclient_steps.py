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

import time
from lettuce import step, world
from xivo_lettuce.xivoclient import start_xivoclient, stop_xivoclient
from xivo_lettuce import common, logs
from xivo_lettuce.manager_ws import user_manager_ws
from xivo_lettuce.manager import cti_client_manager
from hamcrest.core import assert_that
from hamcrest.core.core.isequal import equal_to


@step(u'When I restart the CTI server')
def when_i_restart_the_cti_server(step):
    command = ["/etc/init.d/xivo-ctid", "restart"]
    world.ssh_client_xivo.check_call(command)
    time.sleep(10)


@step(u'When I start the XiVO Client')
def i_start_the_xivo_client(step):
    start_xivoclient()


@step(u'When I start the XiVO Client with an argument "([^"]*)"$')
def i_start_the_xivo_client_with_an_argument(step, argument):
    start_xivoclient(argument)


@step(u'When I stop the XiVO client')
def when_i_stop_the_xivo_client(step):
    stop_xivoclient()


@step(u'Then I get sheet infos')
def get_sheet_infos(step):
    cti_client_manager.get_sheet_infos()


@step(u'I log in the XiVO Client as "([^"]*)", pass "([^"]*)"$')
def i_log_in_the_xivo_client_as_1_pass_2(step, login, password):
    conf_dict = {
        'main_server_address': common.get_host_address(),
        'login': login,
        'password': password
    }
    cti_client_manager.configure_client(conf_dict)
    cti_client_manager.log_in_the_xivo_client()


@step(u'I log in the XiVO Client as "([^"]*)", pass "([^"]*)", unlogged agent$')
def i_log_in_the_xivo_client_as_1_pass_2_unlogged_agent(step, login, password):
    conf_dict = {
        'main_server_address': common.get_host_address(),
        'login': login,
        'password': password,
        'agent_option': 'unlogged'
    }
    cti_client_manager.configure_client(conf_dict)
    cti_client_manager.log_in_the_xivo_client()


@step(u'I log out of the XiVO Client$')
def log_out_of_the_xivo_client(step):
    cti_client_manager.log_out_of_the_xivo_client()


@step(u'When I disable access to XiVO Client to user "([^"]*)" "([^"]*)"')
def when_i_disable_access_to_xivo_client_to_user_group1_group2(step, firstname, lastname):
    user_manager_ws.disable_cti_client(firstname, lastname)
    time.sleep(1)


@step(u'When I enable access to XiVO Client to user "([^"]*)" "([^"]*)"')
def when_i_enable_access_to_xivo_client_to_user_group1_group2(step, firstname, lastname):
    user_manager_ws.enable_cti_client(firstname, lastname)
    time.sleep(1)


@step(u'Then I can\'t connect the CTI client of "([^"]*)" "([^"]*)"')
def then_i_can_t_connect_the_cti_client_of_group1_group2(step, firstname, lastname):
    res = cti_client_manager.log_user_in_client(firstname, lastname)
    assert_that(res['test_result'], equal_to('failed'))


@step(u'Then I can connect the CTI client of "([^"]*)" "([^"]*)"')
def then_i_can_connect_the_cti_client_of_group1_group2(step, firstname, lastname):
    res = cti_client_manager.log_user_in_client(firstname, lastname)
    assert_that(res['test_result'], equal_to('passed'))


@step(u'Then there are no errors in the CTI logs')
def then_there_are_no_errors_in_the_cti_logs(step):
    errors_found = logs.search_str_in_xivo_cti_log("ERROR")
    assert_that(errors_found, equal_to(False), 'errors were found in CTI logs when searching in the directory')
