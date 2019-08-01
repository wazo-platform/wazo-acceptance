# Copyright 2013-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from behave import given

STABLE_URL = 'http://provd.wazo.community/plugins/1/stable/'


@given('the latest plugin "{plugin}" is installed')
def given_the_latest_plugin_is_installed(context, plugin):
    context.helpers.provd.update_plugin_list(STABLE_URL)
    context.helpers.provd.install_latest_plugin(plugin)
