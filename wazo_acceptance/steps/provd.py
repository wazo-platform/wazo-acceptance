# Copyright 2013-2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import json

from behave import given, then
from hamcrest import (
    all_of,
    any_of,
    assert_that,
    has_entries,
    has_entry,
    has_key,
    not_,
)

STABLE_URL = 'http://provd.wazo.community/plugins/1/stable/'


@given('the latest plugin "{plugin}" is installed')
def given_the_latest_plugin_is_installed(context, plugin):
    context.helpers.provd.update_plugin_list(STABLE_URL)
    context.helpers.provd.install_latest_plugin(plugin)


@then('the provd config "{config_id}" has the following values on "{instance}"')
def provd_config_has_the_following_values(context, config_id, instance):
    instance_context = getattr(context.instances, instance)
    config = instance_context.helpers.provd.get_config(config_id)
    slave_host = instance_context.wazo_config.get('slave_host') or '<unknown>'
    for row in context.table:
        expected = row.as_dict()
        expected = _render_expected_config(expected, slave_host)
        assert_that(config, has_entries(expected))


@then('the provd offline config "{config_id}" has the following values on "{instance}"')
def provd_offline_config_has_the_following_values(context, config_id, instance):
    instance_context = getattr(context.instances, instance)
    file_name = f'/var/lib/wazo-provd/jsondb/configs/{config_id}'
    file_content = instance_context.remote_sysutils.get_content_file(file_name)
    config = json.loads(file_content)

    slave_host = instance_context.wazo_config.get('slave_host') or '<unknown>'
    for row in context.table:
        expected = row.as_dict()
        expected = _render_expected_config(expected, slave_host)
        expected_none = {key: value for key, value in expected.items() if value is None}
        expected_values = {key: value for key, value in expected.items() if value is not None}
        assert_that(config, has_keys_absent_or_value_none(expected_none))
        assert_that(config, has_entries(expected_values))


def has_keys_absent_or_value_none(tested):
    matchers = [
        any_of(has_entry(key, None), not_(has_key(key))) for key in tested
    ]
    return all_of(*matchers)


def _render_expected_config(expected, slave_host):
    rendered = {key: value.replace('{{ slave_voip_ip_address }}', slave_host) for key, value in expected.items()}
    rendered = {key: (value or None) for key, value in expected.items()}
    return rendered
