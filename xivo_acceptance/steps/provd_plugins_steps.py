# -*- coding: utf-8 -*-
# Copyright (C) 2013-2015 Avencall
# SPDX-License-Identifier: GPL-3.0-or-later

from hamcrest import assert_that, contains_string
from lettuce import step, world

from xivo_acceptance.action.webi import provd_general as provdg_action_webi
from xivo_acceptance.action.webi import provd_plugins as provdp_action_webi
from xivo_acceptance.lettuce import sysutils

STABLE_URL = 'http://provd.wazo.community/plugins/1/stable/'


@step(u'Given a update plugins provd with good url')
def given_a_update_plugins_provd(step):
    provdp_action_webi.update_plugin_list(STABLE_URL,
                                          check_confirmation=False)


@step(u'Given a update plugins provd with bad url')
def given_a_update_plugins_provd_with_bad_url(step):
    provdp_action_webi.update_plugin_list('http://provd.wazo.community/plugins/1/lol/',
                                          check_confirmation=False)


@step(u'Given there\'s no plugins "([^"]*)" installed')
def given_there_s_no_plugins_group1_installed(step, plugin):
    provdp_action_webi.uninstall_plugins(plugin)


@step(u'Given the plugin "([^"]*)" is installed')
def given_the_plugin_group1_is_installed(step, plugin):
    provdp_action_webi.update_plugin_list(STABLE_URL)
    provdp_action_webi.install_plugin(plugin)


@step(u'Given the latest plugin "([^"]*)" is installed')
def given_the_latest_plugin_group1_is_installed(step, plugin):
    provdp_action_webi.update_plugin_list(STABLE_URL)
    provdp_action_webi.install_latest_plugin(plugin)


@step(u'Given the latest plugin "([^"]*)" for "([^"]*)" is installed')
def given_the_latest_plugin_group1_for_group2_is_installed(step, plugin, model):
    provdp_action_webi.update_plugin_list(STABLE_URL)
    provdp_action_webi.install_latest_plugin(plugin, model)


@step(u'Given the provisioning plugin cache has been cleared')
def given_the_provisioning_plugin_cache_has_been_cleared(step):
    sysutils.send_command(['rm', '-f', '/var/cache/xivo-provd/*'])


@step(u'Given the plugin list has been updated')
def given_the_plugin_list_has_been_updated(step):
    provdp_action_webi.update_plugin_list(STABLE_URL)


@step(u'When I install the latest plugin "([^"]*)"')
def when_i_install_the_latest_plugin_group1(step, plugin):
    provdp_action_webi.install_latest_plugin(plugin)


@step(u'When I install the "([^"]*)" firmware for the latest plugin "([^"]*)"$')
def when_i_install_the_group1_firmware(step, firmware, plugin_prefix):
    plugin_name = provdp_action_webi.get_latest_plugin_name(plugin_prefix)
    provdp_action_webi.install_firmware(plugin_name, firmware)


@step(u'Then plugins list successfully updated')
def then_plugins_list_successfully_updated(step):
    assert provdp_action_webi.plugins_successfully_updated()


@step(u'Then plugins list has a error during update')
def then_plugins_list_has_error_during_update(step):
    assert provdp_action_webi.plugins_error_during_update()
    provdg_action_webi.update_plugin_server_url(STABLE_URL)


@step(u'Then the firmware is successfully installed')
def then_the_group1_firmware_is_successfully_installed(step):
    xpath = "//div[@class[contains(.,'xivo-messages')]]//li"
    message = world.browser.find_element_by_xpath(xpath).text

    expected = "successfully installed"
    assert_that(message, contains_string(expected), "firmware was not successfully installed")
