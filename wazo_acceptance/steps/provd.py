# Copyright 2013-2023 The Wazo Authors  (see the AUTHORS file)
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

STABLE_URL = 'http://provd.wazo.community/plugins/2/stable/'


@given('the plugin "{plugin}" version "{version}" is installed')
def given_the_latest_plugin_is_installed(context, plugin, version):
    context.helpers.provd.update_plugin_list(STABLE_URL)
    context.helpers.provd.install_latest_plugin(f'{plugin}-{version}')


@then('the provd config "{config_id}" has the following values on "{instance}"')
def then_provd_config_has_the_following_values(context, config_id, instance):
    instance_context = getattr(context.instances, instance)
    config = instance_context.helpers.provd.get_config(config_id)
    slave_host = instance_context.wazo_config.get('slave_host') or '<unknown>'
    for row in context.table:
        expected = row.as_dict()
        expected = _render_expected_config(expected, slave_host)
        assert_that(config, has_entries(expected))


@then('the provd offline config "{config_id}" has the following values on "{instance}"')
def then_provd_offline_config_has_the_following_values(context, config_id, instance):
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


@given('the provd HTTP auth strategy is set to "{auth_strategy}"')
def given_provd_http_auth_strategy_is(context, auth_strategy):
    file_name = f'/etc/wazo-provd/conf.d/00-url-key.yml'
    file_content = f'''general:
    http_auth_strategy: {auth_strategy}
    '''
    context.remote_sysutils.write_content_file(file_name, file_content)

    if context.remote_sysutils.is_process_running('wazo-provd'):
        context.remote_sysutils.restart_service('wazo-provd')

    context.add_cleanup(
            context.remote_sysutils.send_command,
            ['rm', '-f', f'{file_name}']
        )
    context.add_cleanup(
        context.remote_sysutils.restart_service,
        'wazo-provd'
    )

@given('the provd tenant provisioning key is "{provisioning_key}')
def given_provd_tenant_provisioning_key_is(context, provisioning_key):
    context.provd_client.params.update('provisioning_key', provisioning_key)


def has_keys_absent_or_value_none(tested):
    matchers = [
        any_of(has_entry(key, None), not_(has_key(key))) for key in tested
    ]
    return all_of(*matchers)


def _render_expected_config(expected, slave_host):
    rendered = {key: value.replace('{{ slave_voip_ip_address }}', slave_host) for key, value in expected.items()}
    rendered = {key: (value or None) for key, value in rendered.items()}
    return rendered
