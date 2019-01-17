# -*- coding: utf-8 -*-
# Copyright (C) 2013-2014 Avencall
# SPDX-License-Identifier: GPL-3.0-or-later

from hamcrest import *
from lettuce.decorators import step
from lettuce.registry import world

from xivo_acceptance.helpers import cti_helper


@step(u'I log in the XiVO Client with bad server address$')
def i_log_in_the_xivo_client_with_bad_server_address(step):
    conf_dict = {
        'main_server_address': 'avencall.com',
        'login': 'toto',
        'password': 'titi'
    }
    cti_helper.configure_client(conf_dict)
    res = cti_helper.log_in_the_xivo_client()
    world.xc_result = res['test_result']


@step(u'I log in the XiVO Client with bad server port$')
def i_log_in_the_xivo_client_with_bad_server_port(step):
    conf_dict = {
        'main_server_port': 123,
        'login': 'toto',
        'password': 'titi'
    }
    cti_helper.configure_client(conf_dict)
    res = cti_helper.log_in_the_xivo_client()
    world.xc_result = res['test_result']


@step(u'When I enable screen pop-up')
def when_i_enable_screen_pop_up(step):
    conf_dict = {'enable_screen_popup': True}
    cti_helper.configure_client(conf_dict)


@step(u'When I enable the hide unlogged agents option')
def when_i_enable_the_hide_unlogged_agents_option(step):
    conf_dict = {'hide_unlogged_agents_for_xlet_queue_members': True}
    cti_helper.configure_client(conf_dict)


@step(u'When I disable the hide unlogged agents option')
def when_i_disable_the_hide_unlogged_agents_option(step):
    conf_dict = {'hide_unlogged_agents_for_xlet_queue_members': False}
    cti_helper.configure_client(conf_dict)


@step(u'When I hide agent option on login screen')
def when_i_hide_agent_option_on_login_screen(step):
    conf_dict = {'show_agent_option': 0}
    cti_helper.configure_client(conf_dict)


@step(u'When I show agent option on login screen')
def when_i_show_agent_option_on_login_screen(step):
    conf_dict = {'show_agent_option': 1}
    cti_helper.configure_client(conf_dict)


@step(u'When I hide profile on status bar')
def when_i_hide_profile_on_status_bar(step):
    conf_dict = {'display_profile': 0}
    cti_helper.configure_client(conf_dict)


@step(u'When I show profile on status bar')
def when_i_show_profile_on_status_bar(step):
    conf_dict = {'display_profile': 1}
    cti_helper.configure_client(conf_dict)


@step(u'When I change my presence to "([^"]*)"')
def when_i_change_my_presence_to_status(step, status):
    cti_helper.set_presence(status)


@step(u'When I enable menu availability')
def when_i_enable_menu_availability(step):
    conf_dict = {'enable_presence_reporting': True}
    cti_helper.configure_client(conf_dict)


@step(u'When I disable menu availability')
def when_i_disable_menu_availability(step):
    conf_dict = {'enable_presence_reporting': False}
    cti_helper.configure_client(conf_dict)


@step(u'When I enable start systrayed')
def when_i_enable_start_systrayed(step):
    conf_dict = {'enable_start_systrayed': True}
    cti_helper.configure_client(conf_dict)


@step(u'When I disable start systrayed')
def when_i_disable_start_systrayed(step):
    conf_dict = {'enable_start_systrayed': False}
    cti_helper.configure_client(conf_dict)


@step(u'When I set auto-reconnect interval to "([^"]*)" seconds')
def when_i_set_auto_reconnect_interval_to_group1_seconds(step, interval):
    conf_dict = {'auto_reconnect_interval': int(interval)}
    cti_helper.configure_client(conf_dict)


@step(u'When I enable auto-reconnect')
def when_i_enable_auto_reconnect(step):
    conf_dict = {'enable_auto_reconnect': True}
    cti_helper.configure_client(conf_dict)


@step(u'When I disable auto-reconnect')
def when_i_disable_auto_reconnect(step):
    conf_dict = {'enable_auto_reconnect': False}
    cti_helper.configure_client(conf_dict)


@step(u'When I enable connect at startup')
def when_i_enable_connect_at_startup(step):
    conf_dict = {'autoconnect': True}
    cti_helper.configure_client(conf_dict)


@step(u'When I disable connect at startup')
def when_i_disable_connect_at_startup(step):
    conf_dict = {'autoconnect': False}
    cti_helper.configure_client(conf_dict)


@step(u'When I enable keep password')
def when_i_enable_keep_password(step):
    conf_dict = {'keep_password': True}
    cti_helper.configure_client(conf_dict)


@step(u'When I enable multiple instances')
def when_i_enable_multiple_instances(step):
    conf_dict = {'enable_multiple_instances': True}
    cti_helper.configure_client(conf_dict)


@step(u'When I disable multiple instances')
def when_i_disable_multiple_instances(step):
    conf_dict = {'enable_multiple_instances': False}
    cti_helper.configure_client(conf_dict)


@step(u'When I set the switchboard queues')
def when_i_set_the_switchboard_queues(step):
    queues = step.hashes[0]
    conf_dict = {'switchboard_incalls_queue': queues['incalls'],
                 'switchboard_on_hold_queue': queues['on hold']}
    cti_helper.configure_client(conf_dict)


@step(u'When I update configuration as "([^"]*)" to "([^"]*)"')
def when_i_update_configuration_as_group1_to_group2(step, conf_key, conf_value):
    conf_dict = {conf_key: conf_value}
    cti_helper.configure_client(conf_dict)


@step(u'Then the configuration "([^"]*)" is equal to "([^"]*)"')
def then_the_configuration_group1_is_equal_to_group2(step, conf_key, conf_value):
    res = cti_helper.get_configuration()
    assert_that(str(res[conf_key]), equal_to(conf_value))


@step(u'Then I not see profile on status bar')
def then_i_not_see_profile_on_status_bar(step):
    res = cti_helper.get_status_bar_infos()
    assert_that(res['return_value']['profilename_is_hidden'], equal_to(True))


@step(u'Then I see profile on status bar')
def then_i_see_profile_on_status_bar(step):
    res = cti_helper.get_status_bar_infos()
    assert_that(res['return_value']['profilename_is_hidden'], equal_to(False))


@step(u'Then I not see agent option on login screen')
def then_i_not_see_agent_option_on_login_screen(step):
    res = cti_helper.get_login_screen_infos()
    assert_that(res['return_value']['show_agent_option'], equal_to(False))


@step(u'Then I see agent option on login screen')
def then_i_see_agent_option_on_login_screen(step):
    res = cti_helper.get_login_screen_infos()
    assert_that(res['return_value']['show_agent_option'], equal_to(True))


@step(u'Then I see a error message on CtiClient')
def then_i_see_a_error_message_on_cticlient(step):
    assert_that(world.xc_result, equal_to('failed'))


@step(u'Then I see menu availability are disabled')
def then_i_see_menu_availability_is_disabled(step):
    res = cti_helper.get_menu_availability_infos()
    assert_that(res['enable'], equal_to(False))


@step(u'Then I see menu availability are enabled')
def then_i_see_menu_availability_is_enabled(step):
    res = cti_helper.get_menu_availability_infos()
    assert_that(res['enable'], equal_to(True))


@step(u'Then I see the window')
def then_i_see_start_systrayed_are_enabled(step):
    res = cti_helper.get_main_window_infos()
    assert_that(res['visible'], equal_to(True))


@step(u'Then I not see the window')
def then_i_see_start_systrayed_are_disabled(step):
    res = cti_helper.get_main_window_infos()
    assert_that(res['visible'], equal_to(False))
