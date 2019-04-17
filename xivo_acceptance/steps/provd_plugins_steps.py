# -*- coding: utf-8 -*-
# Copyright 2013-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from lettuce import step

from xivo_acceptance.helpers import provd_helper as provd
from xivo_acceptance.lettuce import sysutils

STABLE_URL = 'http://provd.wazo.community/plugins/1/stable/'


@step(u'Given a update plugins provd with good url')
def given_a_update_plugins_provd(step):
    provd.update_plugin_list(STABLE_URL)


@step(u'Given a update plugins provd with bad url')
def given_a_update_plugins_provd_with_bad_url(step):
    pass


@step(u'Given there\'s no plugins "([^"]*)" installed')
def given_there_s_no_plugins_group1_installed(step, plugin):
    pass


@step(u'Given the plugin "([^"]*)" is installed')
def given_the_plugin_group1_is_installed(step, plugin):
    pass


@step(u'Given the latest plugin "([^"]*)" is installed')
def given_the_latest_plugin_group1_is_installed(step, plugin):
    provd.update_plugin_list(STABLE_URL)
    provd.install_latest_plugin(plugin)


@step(u'Given the latest plugin "([^"]*)" for "([^"]*)" is installed')
def given_the_latest_plugin_group1_for_group2_is_installed(step, plugin, model):
    pass


@step(u'Given the provisioning plugin cache has been cleared')
def given_the_provisioning_plugin_cache_has_been_cleared(step):
    sysutils.send_command(['rm', '-f', '/var/cache/xivo-provd/*'])


@step(u'Given the plugin list has been updated')
def given_the_plugin_list_has_been_updated(step):
    pass


@step(u'When I install the latest plugin "([^"]*)"')
def when_i_install_the_latest_plugin_group1(step, plugin):
    pass


@step(u'When I install the "([^"]*)" firmware for the latest plugin "([^"]*)"$')
def when_i_install_the_group1_firmware(step, firmware, plugin_prefix):
    pass


@step(u'Then plugins list successfully updated')
def then_plugins_list_successfully_updated(step):
    pass


@step(u'Then plugins list has a error during update')
def then_plugins_list_has_error_during_update(step):
    pass


@step(u'Then the firmware is successfully installed')
def then_the_group1_firmware_is_successfully_installed(step):
    pass
