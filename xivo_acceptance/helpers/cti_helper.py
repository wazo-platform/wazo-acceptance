# -*- coding: utf-8 -*-

# Copyright (C) 2013-2014 Avencall
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
from lettuce.registry import world
from selenium.webdriver.support.select import Select
from xivo_acceptance.helpers import user_helper
from xivo_lettuce import common, sysutils, xivoclient, form

SORT_ASCENDING = 0
SORT_DESCENDING = 1


EVENT_ELEMENT_MAP = {
    'Dial': 'it-dial',
    'Link': 'it-link',
    'Unlink': 'it-unlink',
    'Incoming DID': 'it-incomingdid',
    'Hangup': 'it-hangup',
}


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
    if 'enable_multiple_instances' not in conf_dict:
        conf_dict['enable_multiple_instances'] = True

    return xivoclient.exec_command('configure', conf_dict)


def set_search_for_directory(search):
    res = xivoclient.exec_command('set_search_for_directory', search)
    time.sleep(world.config.xc_login_timeout)
    return res


def set_search_for_remote_directory(search):
    res = xivoclient.exec_command('set_search_for_remote_directory', search)
    time.sleep(world.config.xc_login_timeout)
    return res


def exec_double_click_on_number_for_name(name):
    res = xivoclient.exec_command('exec_double_click_on_number_for_name', name)
    time.sleep(world.config.xc_login_timeout)
    return res


def sort_list_for_remote_directory(column, order=SORT_ASCENDING):
    res = xivoclient.exec_command('sort_list_for_remote_directory', column, order)
    time.sleep(world.config.xc_login_timeout)
    return res


def set_queue_for_queue_members(queue_id):
    res = xivoclient.exec_command('set_queue_for_queue_members', queue_id)
    time.sleep(world.config.xc_login_timeout)
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
    def _to_var_vals(sheet_result):
        res = []
        for var, val in sheet_result.iteritems():
            res.append({u'Variable': var, u'Value': val})
        return res

    try:
        return _to_var_vals(xivoclient.exec_command('get_sheet_infos')['return_value']['content'])
    except KeyError:
        return []


def get_infos_in_custom_sheet():
    response = xivoclient.exec_command('get_infos_in_custom_sheet')
    assert_that(response['test_result'], equal_to('passed'))
    return [{u'widget_name': key, u'value': value} for key, value in response['return_value'].iteritems()]


def set_call_form_model_on_event(call_form_name, event):
    common.open_url('sheetevent')

    for name, element in EVENT_ELEMENT_MAP.iteritems():
        select_box = world.browser.find_element_by_id(element)

        if name == event:
            Select(select_box).select_by_visible_text(call_form_name)
        else:
            Select(select_box).select_by_index(0)

    form.submit.submit_form()


def add_call_form_model(call_form_name, variables):
    common.remove_element_if_exist('sheet', call_form_name)
    common.open_url('sheet', 'add')
    form.input.set_text_field_with_label('Name :', call_form_name)
    common.go_to_tab('Sheet')
    for variable in variables:
        _add_sheet_variable(variable)
    form.submit.submit_form()


def _add_sheet_variable(variable_name):
    var_config = {
        'title': variable_name,
        'display_type': 'text',
        'default_value': '',
        'display_value': '{%s}' % variable_name,
    }
    add_sheet_field(**var_config)


def add_sheet_field(title, display_type, default_value, display_value):
    add_button = world.browser.find_element_by_id('add_variable')
    add_button.click()
    new_variable_line = world.browser.find_element_by_xpath(
        "//tbody[@id='screens']/tr[last()]"
    )

    def _set(column, value):
        xpaths = [
            ".//input[@name='screencol1[]']",
            ".//select[@name='screencol2[]']",
            ".//input[@name='screencol3[]']",
            ".//input[@name='screencol4[]']",
        ]
        widget = new_variable_line.find_element_by_xpath(xpaths[column])
        if column in [0, 2, 3]:
            widget.send_keys(value)
        else:
            Select(widget).select_by_visible_text(value)

    map(_set, xrange(4), [title, display_type, default_value, display_value])


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
    time.sleep(world.config.xc_login_timeout)
    if res['test_result'] == 'passed':
        identity_infos = get_identity_infos()
        world.xc_identity_infos = identity_infos['return_value']
    return res


def log_user_in_client(firstname, lastname):
    user = user_helper.get_by_firstname_lastname(firstname, lastname)
    conf_dict = {
        'main_server_address': common.get_host_address(),
        'main_server_port': 5003,
        'login': user.username,
        'password': user.password
    }
    configure_client(conf_dict)
    return log_in_the_xivo_client()


def restart_server():
    sysutils.restart_service('xivo-ctid')
    time.sleep(10)


def switchboard_answer_incoming_call(cid_name, cid_num):
    response = xivoclient.exec_command('switchboard_answer_incoming_call', cid_name, cid_num)
    assert_that(response['test_result'], equal_to('passed'))


def get_switchboard_current_call_infos():
    response = xivoclient.exec_command('get_switchboard_current_call_infos')
    assert_that(response['test_result'], equal_to('passed'))
    return response['return_value']


def get_switchboard_incoming_calls_infos():
    response = xivoclient.exec_command('get_switchboard_incoming_calls_infos')
    assert_that(response['test_result'], equal_to('passed'))
    return response['return_value']
