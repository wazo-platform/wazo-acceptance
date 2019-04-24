# -*- coding: utf-8 -*-
# Copyright 2013-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from lettuce import step

from xivo_acceptance.helpers import provd_helper as provd

STABLE_URL = 'http://provd.wazo.community/plugins/1/stable/'


@step(u'Given the latest plugin "([^"]*)" is installed')
def given_the_latest_plugin_group1_is_installed(step, plugin):
    provd.update_plugin_list(STABLE_URL)
    provd.install_latest_plugin(plugin)
