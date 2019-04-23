# -*- coding: utf-8 -*-
# Copyright 2013-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import time

from hamcrest import assert_that, equal_to
from lettuce.registry import world
from xivo_acceptance.lettuce import sysutils, xivoclient

SORT_ASCENDING = 0
SORT_DESCENDING = 1


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
    if 'main_server_port' not in conf_dict:
        conf_dict['main_server_port'] = 5003
    if 'enable_multiple_instances' not in conf_dict:
        conf_dict['enable_multiple_instances'] = True

    return xivoclient.exec_command('configure', conf_dict)


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


def get_conference_room_infos():
    return xivoclient.exec_command('get_conference_room_infos')


def get_identity_infos():
    return xivoclient.exec_command('get_identity_infos')


def get_menu_availability_infos():
    return xivoclient.exec_command('get_menu_availability_infos')['return_value']


def set_presence(state):
    return xivoclient.exec_command('set_menu_availability', state)


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
    time.sleep(world.config['xivo_client']['login_timeout'])
    if res['test_result'] == 'passed':
        identity_infos = get_identity_infos()
        world.xc_identity_infos = identity_infos['return_value']
    return res


def restart_server():
    sysutils.restart_service('xivo-ctid')
    time.sleep(10)


def get_switchboard_incoming_calls_infos():
    response = xivoclient.exec_command('get_switchboard_incoming_calls_infos')
    assert_that(response['test_result'], equal_to('passed'))
    return response['return_value']


def dial(extension):
    response = xivoclient.exec_command('dial', extension)
    assert_that(response['test_result'], equal_to('passed'))


def set_dnd(enabled):
    response = xivoclient.exec_command('set_dnd', enabled)
    assert_that(response['test_result'], equal_to('passed'))
    return response


def get_dnd():
    response = xivoclient.exec_command('get_dnd')
    assert_that(response['test_result'], equal_to('passed'))
    return response['return_value']


def set_incallfilter(enabled):
    response = xivoclient.exec_command('set_incallfilter', enabled)
    assert_that(response['test_result'], equal_to('passed'))
    return response


def get_incallfilter():
    response = xivoclient.exec_command('get_incallfilter')
    assert_that(response['test_result'], equal_to('passed'))
    return response['return_value']


def set_noanswer(enabled, destination=''):
    response = xivoclient.exec_command('set_noanswer', enabled, destination)
    assert_that(response['test_result'], equal_to('passed'))
    return response


def get_noanswer():
    response = xivoclient.exec_command('get_noanswer')
    assert_that(response['test_result'], equal_to('passed'))
    return response['return_value']


def set_busy(enabled, destination=''):
    response = xivoclient.exec_command('set_busy', enabled, destination)
    assert_that(response['test_result'], equal_to('passed'))
    return response


def get_busy():
    response = xivoclient.exec_command('get_busy')
    assert_that(response['test_result'], equal_to('passed'))
    return response['return_value']


def set_unconditional(enabled, destination=''):
    response = xivoclient.exec_command('set_unconditional', enabled, destination)
    assert_that(response['test_result'], equal_to('passed'))
    return response


def get_unconditional():
    response = xivoclient.exec_command('get_unconditional')
    assert_that(response['test_result'], equal_to('passed'))
    return response['return_value']


def disable_all_forwards():
    response = xivoclient.exec_command('disable_all_forwards')
    assert_that(response['test_result'], equal_to('passed'))
    return response


def get_disable_all_forwards():
    response = xivoclient.exec_command('get_disable_all_forwards')
    assert_that(response['test_result'], equal_to('passed'))
    return response['return_value']
