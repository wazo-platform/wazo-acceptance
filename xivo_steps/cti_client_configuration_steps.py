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
from lettuce.decorators import step
from xivo_steps.common_xivoclient_steps import i_log_in_the_xivo_client_to_host_1_as_2_pass_3
from lettuce.registry import world
from xivo_lettuce.xivoclient import xivoclient


@step(u'I log in the XiVO Client with bad server address$')
def i_log_in_the_xivo_client_with_server_address_as_1_pass_2(step):
    i_log_in_the_xivo_client_to_host_1_as_2_pass_3('avencall.com',
                                                   'toto',
                                                   'titi')


@xivoclient
def i_log_in_the_xivo_client_to_host_1_as_2_pass_3(host, login, password):
    time.sleep(world.xc_login_timeout)


@step(u'Then I see a error message on CtiClient')
def then_i_see_a_error_message_on_cticlient(step):
    assert world.xc_response.startswith('KO')
