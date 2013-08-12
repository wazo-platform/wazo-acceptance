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


@step(u'I log in the XiVO Client as "([^"]*)", pass "([^"]*)"$')
def i_log_in_the_xivo_client_as_1_pass_2(step, login, password):
    conf_dict = {
        'main_server_address': common.get_host_address(),
        'login': login,
        'password': password,
        'agent_option': 'no',
    }
    cti_client_manager.configure_client(conf_dict)
    result = cti_client_manager.log_in_the_xivo_client()
    assert_that(result['test_result'], equal_to('passed'),
                'could not log in the CTI client as %s pass %s' % (login, password))


@step(u'I log in the XiVO Client as "([^"]*)", pass "([^"]*)", ([a-z]*) agent$')
def i_log_in_the_xivo_client_as_1_pass_2_logged_agent(step, login, password, login_status):
    conf_dict = {
        'main_server_address': common.get_host_address(),
        'login': login,
        'password': password,
        'agent_option': login_status,
    }
    cti_client_manager.configure_client(conf_dict)
    result = cti_client_manager.log_in_the_xivo_client()
    assert_that(result['test_result'], equal_to('passed'),
                'could not log in the CTI client as %s pass %s' % (login, password))


@step(u'I log out of the XiVO Client$')
def log_out_of_the_xivo_client(step):
    cti_client_manager.log_out_of_the_xivo_client()


@step(u'When I restart the CTI server')
def when_i_restart_the_cti_server(step):
    command = ["/etc/init.d/xivo-ctid", "restart"]
    world.ssh_client_xivo.check_call(command)
    time.sleep(10)


@step(u'When I start the XiVO Client$')
def i_start_the_xivo_client(step):
    start_xivoclient()


@step(u'When I start the XiVO Client "([^"]*)"$')
def i_start_the_xivo_client_xxx(step, instance_name):
    start_xivoclient('', name=instance_name)


@step(u'When I start the XiVO Client with an argument "([^"]*)"$')
def i_start_the_xivo_client_with_an_argument(step, argument):
    start_xivoclient(argument)


@step(u'When I stop the XiVO client$')
def when_i_stop_the_xivo_client(step):
    stop_xivoclient()


@step(u'When I stop the XiVO client "([^"]*)"$')
def when_i_stop_the_xivo_client_xxx(step, instance_name):
    stop_xivoclient(instance_name)


@step(u'When I enable menu availability')
def when_i_enable_menu_availability(step):
    conf_dict = {'enable_presence_reporting': True}
    cti_client_manager.configure_client(conf_dict)


@step(u'When I disable menu availability')
def when_i_disable_menu_availability(step):
    conf_dict = {'enable_presence_reporting': False}
    cti_client_manager.configure_client(conf_dict)


@step(u'When I enable start systrayed')
def when_i_enable_start_systrayed(step):
    conf_dict = {'enable_start_systrayed': True}
    cti_client_manager.configure_client(conf_dict)


@step(u'When I disable start systrayed')
def when_i_disable_start_systrayed(step):
    conf_dict = {'enable_start_systrayed': False}
    cti_client_manager.configure_client(conf_dict)


@step(u'When I set auto-reconnect interval to "([^"]*)" seconds')
def when_i_set_auto_reconnect_interval_to_group1_seconds(step, interval):
    conf_dict = {'auto_reconnect_interval': int(interval)}
    cti_client_manager.configure_client(conf_dict)


@step(u'When I enable auto-reconnect')
def when_i_enable_auto_reconnect(step):
    conf_dict = {'enable_auto_reconnect': True}
    cti_client_manager.configure_client(conf_dict)


@step(u'When I disable auto-reconnect')
def when_i_disable_auto_reconnect(step):
    conf_dict = {'enable_auto_reconnect': False}
    cti_client_manager.configure_client(conf_dict)


@step(u'When I enable connect at startup')
def when_i_enable_connect_at_startup(step):
    conf_dict = {'autoconnect': True}
    cti_client_manager.configure_client(conf_dict)


@step(u'When I disable connect at startup')
def when_i_disable_connect_at_startup(step):
    conf_dict = {'autoconnect': False}
    cti_client_manager.configure_client(conf_dict)


@step(u'When I enable keep password')
def when_i_enable_keep_password(step):
    conf_dict = {'keep_password': True}
    cti_client_manager.configure_client(conf_dict)


@step(u'When I disable access to XiVO Client to user "([^"]*)" "([^"]*)"')
def when_i_disable_access_to_xivo_client_to_user_group1_group2(step, firstname, lastname):
    user_manager_ws.disable_cti_client(firstname, lastname)
    time.sleep(1)


@step(u'When I enable access to XiVO Client to user "([^"]*)" "([^"]*)"')
def when_i_enable_access_to_xivo_client_to_user_group1_group2(step, firstname, lastname):
    user_manager_ws.enable_cti_client(firstname, lastname)
    time.sleep(1)


@step(u'When I log in and log out of the XiVO Client as "([^"]*)", pass "([^"]*)" (\d+) times')
def when_i_log_in_and_log_out_of_the_xivo_client_as_group1_pass_group2_10_times(step, username, password, count):
    for i in range(int(count)):
        step.when('I log in the XiVO Client as "%s", pass "%s"' % (username, password))
        time.sleep(2)
        step.when('I log out of the XiVO Client')


@step(u'When I enable multiple instances')
def when_i_enable_multiple_instances(step):
    conf_dict = {'enable_multiple_instances': True}
    cti_client_manager.configure_client(conf_dict)


@step(u'When I disable multiple instances')
def when_i_disable_multiple_instances(step):
    conf_dict = {'enable_multiple_instances': False}
    cti_client_manager.configure_client(conf_dict)


@step(u'Then I have "([^"]*)" instances of the client')
def then_i_have_x_instances_of_the_client(step, nb_instances):
    assert_that(cti_client_manager.get_nb_instances(), equal_to(int(nb_instances)))


@step(u'Then I logged after "([^"]*)" seconds')
def then_i_logged_after_x_seconds(step, wait_seconds):
    time.sleep(int(wait_seconds))
    assert_that(cti_client_manager.is_logged(), equal_to(True))


@step(u'Then I not logged after "([^"]*)" seconds')
def then_i_not_logged_after_x_seconds(step, wait_seconds):
    time.sleep(int(wait_seconds))
    assert_that(cti_client_manager.is_logged(), equal_to(False))


@step(u'Then I see menu availability are disabled')
def then_i_see_menu_availability_is_disabled(step):
    res = cti_client_manager.get_menu_availability_infos()
    assert_that(res['enable'], equal_to(False))


@step(u'Then I see menu availability are enabled')
def then_i_see_menu_availability_is_enabled(step):
    res = cti_client_manager.get_menu_availability_infos()
    assert_that(res['enable'], equal_to(True))


@step(u'Then I see the window')
def then_i_see_start_systrayed_are_enabled(step):
    res = cti_client_manager.get_main_window_infos()
    assert_that(res['visible'], equal_to(True))


@step(u'Then I not see the window')
def then_i_see_start_systrayed_are_disabled(step):
    res = cti_client_manager.get_main_window_infos()
    assert_that(res['visible'], equal_to(False))


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


@step(u'Then the XiVO Client did not crash')
def then_the_xivo_client_does_not_crash(step):
    pass
