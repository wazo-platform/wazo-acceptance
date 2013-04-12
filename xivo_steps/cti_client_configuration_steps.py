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


@step(u'I log in the XiVO Client with bad server address$')
def i_log_in_the_xivo_client_with_bad_server_address(step):
    conf_dict = {
        'main_server_address': 'avencall.com',
        'login': 'toto',
        'password': 'titi'
    }
    cti_client_manager.configure_client(conf_dict)
    cti_client_manager.log_in_the_xivo_client()


@step(u'When I enable screen pop-up')
def when_i_enable_screen_pop_up(step):
    conf_dict = {'customerinfo': True}
    cti_client_manager.configure_client(conf_dict)
    assert world.xc_response == 'passed'


@step(u'When I enable the hide unlogged agents option')
def when_i_enable_the_hide_unlogged_agents_option(step):
    conf_dict = {'hide_unlogged_agents_for_xlet_queue_members': True}
    cti_client_manager.configure_client(conf_dict)
    assert world.xc_response == 'passed'


@step(u'When I disable the hide unlogged agents option')
def when_i_disable_the_hide_unlogged_agents_option(step):
    conf_dict = {'hide_unlogged_agents_for_xlet_queue_members': False}
    cti_client_manager.configure_client(conf_dict)
    assert world.xc_response == 'passed'


@step(u'Then I see a error message on CtiClient')
def then_i_see_a_error_message_on_cticlient(step):
    assert world.xc_response == 'failed'
