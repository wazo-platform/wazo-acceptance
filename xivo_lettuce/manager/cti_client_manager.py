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
from xivo_lettuce import common, xivoclient


def configure_client(conf_dict):
    """
    conf_dict = {
        'main_server_address': 'string',
        'main_server_port': int,
        'login': 'string',
        'password': 'string',
        'agent_option': enum [no, unlogged, logged]
        'show_agent_option': bool
    }
    """
    if 'main_server_address' not in conf_dict:
        conf_dict['main_server_address'] = common.get_host_address()
    if 'main_server_port' not in conf_dict:
        conf_dict['main_server_port'] = 5003
    if 'show_agent_option' not in conf_dict:
        conf_dict['show_agent_option'] = False

    from pprint import pprint
    pprint(conf_dict)

    @xivoclient
    def configure(conf_dict):
        time.sleep(world.xc_login_timeout)
    configure(conf_dict)
