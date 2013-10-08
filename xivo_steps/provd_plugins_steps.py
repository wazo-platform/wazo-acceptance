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

from hamcrest import assert_that, contains_string
from lettuce import step, world

from xivo_lettuce.manager_webi import provd_general_manager as provdg
from xivo_lettuce.manager_webi import provd_plugins_manager as provdp
from xivo_lettuce import sysutils


@step(u'Given a update plugins provd with good url')
def given_a_update_plugins_provd(step):
    provdp.update_plugin_list('http://provd.xivo.fr/plugins/1/stable/',
                              check_confirmation=False)


@step(u'Given a update plugins provd with bad url')
def given_a_update_plugins_provd_with_bad_url(step):
    provdp.update_plugin_list('http://provd.xivo.fr/plugins/1/lol/',
                              check_confirmation=False)


@step(u'Given the plugin "([^"]*)" is not installed')
def given_the_plugin_group1_is_not_installed(step, plugin):
    provdp.uninstall_plugin(plugin)


@step(u'Given the plugin "([^"]*)" is installed')
def given_the_plugin_group1_is_installed(step, plugin):
    provdp.update_plugin_list('http://provd.xivo.fr/plugins/1/stable/')
    provdp.install_plugin(plugin)


@step(u'Given the provisionning plugin cache has been cleared')
def given_the_provisionning_plugin_cache_has_been_cleared(step):
    sysutils.send_command(['rm', '-f', '/var/cache/xivo-provd/*'])


@step(u'Given the plugin list has been updated')
def given_the_plugin_list_has_been_updated(step):
    provdp.update_plugin_list('http://provd.xivo.fr/plugins/1/stable/')


@step(u'When I install the plugin "([^"]*)"')
def when_i_install_the_plugin_group1(step, plugin):
    provdp.install_plugin(plugin)


@step(u'When I install the "([^"]*)" firmware')
def when_i_install_the_group1_firmware(step, firmware):
    provdp.install_firmware(firmware)


@step(u'Then plugins list successfully updated')
def then_plugins_list_successfully_updated(step):
    assert provdp.plugins_successfully_updated()


@step(u'Then plugins list has a error during update')
def then_plugins_list_has_error_during_update(step):
    assert provdp.plugins_error_during_update()
    provdg.update_plugin_server_url('http://provd.xivo.fr/plugins/1/stable/')


@step(u'Then the firmware is successfully installed')
def then_the_group1_firmware_is_successfully_installed(step):
    xpath = "//div[@class[contains(.,'xivo-messages')]]//li"
    message = world.browser.find_element_by_xpath(xpath).text

    expected = "successfully installed"
    assert_that(message, contains_string(expected), "firmware was not successfully installed")
