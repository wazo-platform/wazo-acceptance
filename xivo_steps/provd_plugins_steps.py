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

from hamcrest import assert_that, contains_string
from lettuce import step, world

from xivo_acceptance.action.webi import provd_general as provdg_action_webi
from xivo_acceptance.action.webi import provd_plugins as provdp_action_webi
from xivo_lettuce import sysutils


@step(u'Given a update plugins provd with good url')
def given_a_update_plugins_provd(step):
    provdp_action_webi.update_plugin_list('http://provd.xivo.fr/plugins/1/stable/',
                                          check_confirmation=False)


@step(u'Given a update plugins provd with bad url')
def given_a_update_plugins_provd_with_bad_url(step):
    provdp_action_webi.update_plugin_list('http://provd.xivo.fr/plugins/1/lol/',
                                          check_confirmation=False)


@step(u'Given the plugin "([^"]*)" is not installed')
def given_the_plugin_group1_is_not_installed(step, plugin):
    provdp_action_webi.uninstall_plugin(plugin)


@step(u'Given there\'s no plugins "([^"]*)" installed')
def given_there_s_no_plugins_group1_installed(step, plugin):
    provdp_action_webi.uninstall_plugins(plugin)


@step(u'Given the plugin "([^"]*)" is installed')
def given_the_plugin_group1_is_installed(step, plugin):
    provdp_action_webi.update_plugin_list('http://provd.xivo.fr/plugins/1/stable/')
    provdp_action_webi.install_plugin(plugin)


@step(u'Given the provisioning plugin cache has been cleared')
def given_the_provisioning_plugin_cache_has_been_cleared(step):
    sysutils.send_command(['rm', '-f', '/var/cache/xivo-provd/*'])


@step(u'Given the plugin list has been updated')
def given_the_plugin_list_has_been_updated(step):
    provdp_action_webi.update_plugin_list('http://provd.xivo.fr/plugins/1/stable/')


@step(u'When I install the plugin "([^"]*)"')
def when_i_install_the_plugin_group1(step, plugin):
    provdp_action_webi.install_plugin(plugin)


@step(u'When I install the latest plugin "([^"]*)"')
def when_i_install_the_latest_plugin_group1(step, plugin):
    provdp_action_webi.install_latest_plugin(plugin)


@step(u'When I install the "([^"]*)" firmware')
def when_i_install_the_group1_firmware(step, firmware):
    provdp_action_webi.install_firmware(firmware)


@step(u'Then plugins list successfully updated')
def then_plugins_list_successfully_updated(step):
    assert provdp_action_webi.plugins_successfully_updated()


@step(u'Then plugins list has a error during update')
def then_plugins_list_has_error_during_update(step):
    assert provdp_action_webi.plugins_error_during_update()
    provdg_action_webi.update_plugin_server_url('http://provd.xivo.fr/plugins/1/stable/')


@step(u'Then the firmware is successfully installed')
def then_the_group1_firmware_is_successfully_installed(step):
    xpath = "//div[@class[contains(.,'xivo-messages')]]//li"
    message = world.browser.find_element_by_xpath(xpath).text

    expected = "successfully installed"
    assert_that(message, contains_string(expected), "firmware was not successfully installed")
