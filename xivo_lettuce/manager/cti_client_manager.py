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


from xivo_lettuce import common, xivoclient
from xivo_lettuce.manager_ws import user_manager_ws
import time
from lettuce.registry import world


def configure_client(conf_dict):
    """This function send a message to cticlient to configure it.

    :param conf_dict: The dict to configure.
    :type conf_dict: dict
    :example:

    .. code-block:: javascript

        conf_dict = {
            'main_server_address': char,
            'main_server_port': int,
            'main_server_encrypted': boolean,
            'backup_server_address': char,
            'backup_server_port': int,
            'backup_server_encrypted': boolean,
            'login': char,
            'password': char,
            'keep_password': boolean,
            'display_profile': boolean,
            'autoconnect': boolean,
            'show_agent_option': boolean,
            'agent_option': enum [no, unlogged, logged],
            'hide_unlogged_agents_for_xlet_queue_members': boolean,
            'enable_screen_popup': boolean,
            'enable_presence_reporting': boolean,
            'enable_start_systrayed': boolean,
            'enable_auto_reconnect': boolean,
            'auto_reconnect_interval': int,
            'enable_multiple_instances': boolean
        }

    """
    if 'main_server_address' not in conf_dict:
        conf_dict['main_server_address'] = common.get_host_address()
    if 'main_server_port' not in conf_dict:
        conf_dict['main_server_port'] = 5003

    return xivoclient.exec_command('configure', conf_dict)


def set_search_for_directory(search):
    res = xivoclient.exec_command('set_search_for_directory', search)
    time.sleep(world.xc_login_timeout)
    return res


def set_search_for_remote_directory(search):
    res = xivoclient.exec_command('set_search_for_remote_directory', search)
    time.sleep(world.xc_login_timeout)
    return res


def exec_double_click_on_number_for_name(name):
    res = xivoclient.exec_command('exec_double_click_on_number_for_name', name)
    time.sleep(world.xc_login_timeout)
    return res


def set_queue_for_queue_members(queue_id):
    res = xivoclient.exec_command('set_queue_for_queue_members', queue_id)
    time.sleep(world.xc_login_timeout)
    return res


def get_configuration():
    res = xivoclient.exec_command('get_configuration')
    return res['return_value']


def get_xlets():
    res = xivoclient.exec_command('get_xlets')
    return res['return_value']


def get_login_screen_infos():
    return xivoclient.exec_command('get_login_screen_infos')


def get_status_bar_infos():
    return xivoclient.exec_command('get_status_bar_infos')


def get_remote_directory_infos():
    return xivoclient.exec_command('get_remote_directory_infos')


def get_switchboard_infos():
    return xivoclient.exec_command('get_switchboard_infos')


def get_conference_room_infos():
    return xivoclient.exec_command('get_conference_room_infos')


def get_identity_infos():
    return xivoclient.exec_command('get_identity_infos')


def get_sheet_infos():
    return xivoclient.exec_command('get_sheet_infos')


def get_queue_members_infos():
    return xivoclient.exec_command('get_queue_members_infos')


def get_agent_list_infos():
    return xivoclient.exec_command('get_agent_list_infos')['return_value']


def get_menu_availability_infos():
    return xivoclient.exec_command('get_menu_availability_infos')['return_value']


def get_main_window_infos():
    return xivoclient.exec_command('get_main_window_infos')['return_value']


def log_out_of_the_xivo_client():
    return xivoclient.exec_command('i_log_out_of_the_xivo_client')


def is_logged():
    res = xivoclient.exec_command('is_logged')
    return bool(res['return_value']['logged'])


def get_nb_instances():
    return len(world.xc_process_dict)


def log_in_the_xivo_client():
    res = xivoclient.exec_command('i_log_in_the_xivo_client')
    time.sleep(world.xc_login_timeout)
    if res['test_result'] == 'passed':
        identity_infos = get_identity_infos()
        world.xc_identity_infos = identity_infos['return_value']
    return res


def log_user_in_client(firstname, lastname):
    user = user_manager_ws.find_user_with_firstname_lastname(firstname, lastname)
    conf_dict = {
        'main_server_address': common.get_host_address(),
        'main_server_port': 5003,
        'login': user.client_username,
        'password': user.client_password
    }
    configure_client(conf_dict)
    return log_in_the_xivo_client()
