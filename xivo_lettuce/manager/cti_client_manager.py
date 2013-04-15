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
from lettuce import world
from xivo_lettuce import common
from xivo_lettuce.manager_ws import user_manager_ws
from xivo_lettuce.xivoclient import xivoclient
from hamcrest.core import assert_that
from hamcrest.core.core.isequal import equal_to


def configure_client(conf_dict):
    """
    conf_dict = {
        'main_server_address': 'string',
        'main_server_port': int,
        'login': 'string',
        'password': 'string',
        'agent_option': enum [no, unlogged, logged]
        'hide_unlogged_agents_for_xlet_queue_members': bool
    }
    """
    if 'main_server_address' not in conf_dict:
        conf_dict['main_server_address'] = common.get_host_address()
    if 'main_server_port' not in conf_dict:
        conf_dict['main_server_port'] = 5003

    @xivoclient
    def configure(conf_dict):
        time.sleep(world.xc_login_timeout)
    configure(conf_dict)
    assert_that(world.xc_response, equal_to('passed'))


@xivoclient
def get_identity_infos():
    assert_that(world.xc_response, equal_to('passed'))


@xivoclient
def get_sheet_infos():
    assert_that(world.xc_response, equal_to('passed'))


@xivoclient
def set_queue_for_queue_members(queue_id):
    assert_that(world.xc_response, equal_to('passed'))


@xivoclient
def get_queue_members_infos():
    assert_that(world.xc_response, equal_to('passed'))


def log_out_of_the_xivo_client():
    @xivoclient
    def i_log_out_of_the_xivo_client():
        pass
    i_log_out_of_the_xivo_client()


def log_in_the_xivo_client():
    @xivoclient
    def i_log_in_the_xivo_client():
        time.sleep(world.xc_login_timeout)
    i_log_in_the_xivo_client()
    if world.xc_response == 'passed':
        get_identity_infos()


def log_user_in_client(firstname, lastname):
    user = user_manager_ws.find_user_with_firstname_lastname(firstname, lastname)
    conf_dict = {
        'main_server_address': common.get_host_address(),
        'main_server_port': 5003,
        'login': user.client_username,
        'password': user.client_password
    }
    configure_client(conf_dict)
    log_in_the_xivo_client()
