# Copyright 2013-2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from behave import given, then
from hamcrest import assert_that, has_entries

STABLE_URL = 'http://provd.wazo.community/plugins/1/stable/'


@given('the latest plugin "{plugin}" is installed')
def given_the_latest_plugin_is_installed(context, plugin):
    context.helpers.provd.update_plugin_list(STABLE_URL)
    context.helpers.provd.install_latest_plugin(plugin)


@then('the provd config "{config_id}" has the following values')
def step_impl(context, config_id):
    config = context.helpers.provd.get_config(config_id)
    for row in context.table:
        assert_that(config, has_entries(**row.as_dict()))
