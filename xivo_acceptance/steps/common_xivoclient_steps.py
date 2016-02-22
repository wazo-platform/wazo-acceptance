# -*- coding: utf-8 -*-

# Copyright (C) 2013-2016 Avencall
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

from hamcrest import assert_that, equal_to
from lettuce import step

from xivo_acceptance.helpers import user_helper, cti_helper
from xivo_acceptance.lettuce import common
from xivo_acceptance.lettuce import xivoclient


@step(u'I log in the XiVO Client as "([^"]*)", pass "([^"]*)"$')
def i_log_in_the_xivo_client_as_1_pass_2(step, login, password):
    conf_dict = {
        'main_server_address': common.get_host_address(),
        'login': login,
        'password': password,
        'agent_option': 'no',
    }
    cti_helper.configure_client(conf_dict)
    result = cti_helper.log_in_the_xivo_client()
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
    cti_helper.configure_client(conf_dict)
    result = cti_helper.log_in_the_xivo_client()
    assert_that(result['test_result'], equal_to('passed'),
                'could not log in the CTI client as %s pass %s' % (login, password))


@step(u'I log out of the XiVO Client$')
def log_out_of_the_xivo_client(step):
    cti_helper.log_out_of_the_xivo_client()


@step(u'I start the XiVO Client$')
def i_start_the_xivo_client(step):
    xivoclient.start_xivoclient()


@step(u'When I start the XiVO Client "([^"]*)"$')
def i_start_the_xivo_client_xxx(step, instance_name):
    xivoclient.start_xivoclient(name=instance_name)


@step(u'When I start the XiVO Client "([^"]*)" with errors$')
def i_start_the_xivo_client_xxx_with_errors(step, instance_name):
    xivoclient.start_xivoclient_with_errors(name=instance_name)


@step(u'When I start the XiVO Client with an argument "([^"]*)"$')
def i_start_the_xivo_client_with_an_argument(step, argument):
    xivoclient.start_xivoclient(argument)


@step(u'When I stop the XiVO client$')
def when_i_stop_the_xivo_client(step):
    xivoclient.stop_xivoclient()


@step(u'When I stop the XiVO client "([^"]*)"$')
def when_i_stop_the_xivo_client_xxx(step, instance_name):
    xivoclient.stop_xivoclient(instance_name)


@step(u'When I disable access to XiVO Client to user "([^"]*)" "([^"]*)"')
def when_i_disable_access_to_xivo_client_to_user_group1_group2(step, firstname, lastname):
    user_helper.disable_cti_client(firstname, lastname)
    time.sleep(1)


@step(u'When I enable access to XiVO Client to user "([^"]*)" "([^"]*)"')
def when_i_enable_access_to_xivo_client_to_user_group1_group2(step, firstname, lastname):
    user_helper.enable_cti_client(firstname, lastname)
    time.sleep(1)


@step(u'When I log in and log out of the XiVO Client as "([^"]*)", pass "([^"]*)" (\d+) times')
def when_i_log_in_and_log_out_of_the_xivo_client_as_group1_pass_group2_10_times(step, username, password, count):
    for i in range(int(count)):
        step.when('I log in the XiVO Client as "%s", pass "%s"' % (username, password))
        time.sleep(2)
        step.when('I log out of the XiVO Client')


@step(u'When I dial "([^"]*)" with the XiVO Client')
def when_i_dial_1_with_the_xivo_client(step, extension):
    cti_helper.dial(extension)


@step(u'Then I have "([^"]*)" instances of the client')
def then_i_have_x_instances_of_the_client(step, nb_instances):
    assert_that(cti_helper.get_nb_instances(), equal_to(int(nb_instances)))


@step(u'Then I logged after "([^"]*)" seconds')
def then_i_logged_after_x_seconds(step, wait_seconds):
    time.sleep(int(wait_seconds))
    assert_that(cti_helper.is_logged(), equal_to(True))


@step(u'Then I not logged after "([^"]*)" seconds')
def then_i_not_logged_after_x_seconds(step, wait_seconds):
    time.sleep(int(wait_seconds))
    assert_that(cti_helper.is_logged(), equal_to(False))


@step(u'Then I can\'t connect the CTI client of "([^"]*)" "([^"]*)"')
def then_i_can_t_connect_the_cti_client_of_group1_group2(step, firstname, lastname):
    res = cti_helper.log_user_in_client(firstname, lastname)
    assert_that(res['test_result'], equal_to('failed'))


@step(u'Then I can connect the CTI client of "([^"]*)" "([^"]*)"')
def then_i_can_connect_the_cti_client_of_group1_group2(step, firstname, lastname):
    res = cti_helper.log_user_in_client(firstname, lastname)
    assert_that(res['test_result'], equal_to('passed'))


@step(u'Then the XiVO Client did not crash')
def then_the_xivo_client_does_not_crash(step):
    pass
