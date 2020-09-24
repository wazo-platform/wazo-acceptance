# Copyright 2013-2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import json

from behave import given, then
from hamcrest import assert_that, equal_to, has_entries

STABLE_URL = 'http://provd.wazo.community/plugins/1/stable/'


@given('the latest plugin "{plugin}" is installed')
def given_the_latest_plugin_is_installed(context, plugin):
    context.helpers.provd.update_plugin_list(STABLE_URL)
    context.helpers.provd.install_latest_plugin(plugin)


@then('the provd config "{config_id}" has the following values on "{instance}"')
def provd_config_has_the_following_values(context, config_id, instance):
    instance_context = getattr(context.instances, instance)
    config = instance_context.helpers.provd.get_config(config_id)
    for row in context.table:
        expected = row.as_dict()
        for key, value in expected.items():
            if '{{ slave_voip_ip_address }}' in value:
                rendered_value = value.replace(
                    '{{ slave_voip_ip_address }}',
                    instance_context.wazo_config.get('slave_host') or '<unknown>',
                )
                assert_that(config.get(key, ''), equal_to(rendered_value))


@then('the provd offline config "{config_id}" has the following values on "{instance}"')
def provd_offline_config_has_the_following_values(context, config_id, instance):
    instance_context = getattr(context.instances, instance)
    file_name = f'/var/lib/wazo-provd/jsondb/configs/{config_id}'
    file_content = instance_context.remote_sysutils.get_content_file(file_name)
    config = json.loads(file_content)

    slave_host = instance_context.wazo_config.get('slave_host') or '<unknown>'
    for row in context.table:
        expected = row.as_dict()
        expected = {key: value.replace('{{ slave_voip_ip_address }}', slave_host) for key, value in expected.items()}
        expected = {key: (value or None) for key, value in expected.items()}
        assert_that(config, has_entries(expected))
