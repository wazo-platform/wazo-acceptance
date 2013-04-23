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


from lettuce.decorators import step
from lettuce.registry import world
from xivo_lettuce.manager import cti_client_manager
from hamcrest.core import assert_that
from hamcrest.core.core.isequal import equal_to


@step(u'I log in the XiVO Client with bad server address$')
def i_log_in_the_xivo_client_with_bad_server_address(step):
    conf_dict = {
        'main_server_address': 'avencall.com',
        'login': 'toto',
        'password': 'titi'
    }
    cti_client_manager.configure_client(conf_dict)
    cti_client_manager.log_in_the_xivo_client()


@step(u'I log in the XiVO Client with bad server port$')
def i_log_in_the_xivo_client_with_bad_server_port(step):
    conf_dict = {
        'main_server_port': 123,
        'login': 'toto',
        'password': 'titi'
    }
    cti_client_manager.configure_client(conf_dict)
    cti_client_manager.log_in_the_xivo_client()


@step(u'When I enable screen pop-up')
def when_i_enable_screen_pop_up(step):
    conf_dict = {'customerinfo': True}
    cti_client_manager.configure_client(conf_dict)


@step(u'When I enable the hide unlogged agents option')
def when_i_enable_the_hide_unlogged_agents_option(step):
    conf_dict = {'hide_unlogged_agents_for_xlet_queue_members': True}
    cti_client_manager.configure_client(conf_dict)


@step(u'When I disable the hide unlogged agents option')
def when_i_disable_the_hide_unlogged_agents_option(step):
    conf_dict = {'hide_unlogged_agents_for_xlet_queue_members': False}
    cti_client_manager.configure_client(conf_dict)


@step(u'When I hide agent option on login screen')
def when_i_hide_agent_option_on_login_screen(step):
    conf_dict = {
        'show_agent_option': 0,
    }
    cti_client_manager.configure_client(conf_dict)


@step(u'When I show agent option on login screen')
def when_i_show_agent_option_on_login_screen(step):
    conf_dict = {
        'show_agent_option': 1,
    }
    cti_client_manager.configure_client(conf_dict)


@step(u'Then I not see agent option on login screen')
def then_i_not_see_agent_option_on_login_screen(step):
    cti_client_manager.get_login_screen_infos()
    assert_that(world.xc_return_value['show_agent_option'], equal_to(False))


@step(u'Then I see agent option on login screen')
def then_i_see_agent_option_on_login_screen(step):
    cti_client_manager.get_login_screen_infos()
    assert_that(world.xc_return_value['show_agent_option'], equal_to(True))


@step(u'Then I see a error message on CtiClient')
def then_i_see_a_error_message_on_cticlient(step):
    assert_that(world.xc_response, equal_to('failed'))
