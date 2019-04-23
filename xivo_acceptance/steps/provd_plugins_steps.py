# -*- coding: utf-8 -*-
# Copyright 2013-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from lettuce import step

from xivo_acceptance.helpers import provd_helper as provd

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


@step(u'Given the latest plugin "([^"]*)" is installed')
def given_the_latest_plugin_group1_is_installed(step, plugin):
    provd.update_plugin_list(STABLE_URL)
    provd.install_latest_plugin(plugin)


@step(u'Then plugins list successfully updated')
def then_plugins_list_successfully_updated(step):
    pass


@step(u'Then plugins list has a error during update')
def then_plugins_list_has_error_during_update(step):
    pass
