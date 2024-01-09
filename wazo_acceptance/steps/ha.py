# Copyright 2019-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import string

from datetime import datetime, timezone

from behave import given, when, then, step
from wazo_test_helpers import until

from wazo_acceptance import auth, setup


@given('the HA is enabled as master on "{instance}"')
def given_the_ha_is_enabled_as_master_on_instance(context, instance):
    context = getattr(context.instances, instance)
    context.confd_client.ha.update({
        'node_type': 'master',
        'remote_address': context.wazo_config['slave_host']
    })


@given('the HA is enabled as slave on "{instance}"')
def given_the_ha_is_enabled_as_slave(context, instance):
    context = getattr(context.instances, instance)
    context.confd_client.ha.update({
        'node_type': 'slave',
        'remote_address': context.wazo_config['master_host']
    })


@given('there is a user "{username}" on "{instance}"')
def given_there_is_a_user_username_on_instance(context, username, instance):
    context = getattr(context.instances, instance)
    body = {
        'username': username,
        'password': context.helpers.utils.random_string(10, sample=string.printable),
    }
    context.helpers.user.create(body)


@given('there is no user "{username}" on "{instance}"')
def given_there_is_no_user_username_on_instance(context, username, instance):
    context = getattr(context.instances, instance)
    users = context.auth_client.users.list(username=username)['items']
    if users:
        for user in users:
            context.auth_client.users.delete(user['uuid'])


@when('I disable the HA on "{instance}"')
def when_i_disable_the_ha_on_instance(context, instance):
    context = getattr(context.instances, instance)
    context.confd_client.ha.update({
        'node_type': 'disabled',
    })


@when('I enable the HA as master on "{instance}"')
def when_i_enable_the_ha_as_master_on_instance(context, instance):
    context = getattr(context.instances, instance)
    context.confd_client.ha.update({
        'node_type': 'master',
        'remote_address': context.wazo_config['slave_host']
    })


@when('I enable the HA as slave on "{instance}"')
def when_i_enable_the_ha_as_slave_on_instance(context, instance):
    context = getattr(context.instances, instance)
    context.confd_client.ha.update({
        'node_type': 'slave',
        'remote_address': context.wazo_config['master_host']
    })


@when('I start the replication from "{instance_master}" to "{instance_slave}"')
def when_i_start_the_replication_from_instancemaster_to_instanceslave(context, instance_master, instance_slave):
    master_context = getattr(context.instances, instance_master)
    slave_host = master_context.wazo_config['slave_host']
    master_context.remote_sysutils.send_command(['xivo-master-slave-db-replication', slave_host], check=True)
    slave_context = getattr(context.instances, instance_slave)
    auth.renew_auth_token(slave_context)
    setup.setup_tenant(slave_context)


@when('I start the replication from "{instance_master}" to unknown')
def when_i_start_the_replication_from_instancemaster_to_unknown(context, instance_master):
    master_context = getattr(context.instances, instance_master)
    context.mail_start_time = datetime.now(tz=timezone.utc)
    invalid_ip = '198.51.100.1'
    command = ['xivo-master-slave-db-replication', invalid_ip]
    master_context.remote_sysutils.send_command(command, check=False)


@then('there is a user "{username}" on "{instance}"')
def then_there_is_a_user_username_on_instance(context, username, instance):
    context = getattr(context.instances, instance)
    assert context.helpers.user.get_by(username=username)


@then('there is a mail with content "{content}" on "{instance}"')
def then_there_is_a_mail_with_content_on_instance(context, content, instance):
    try:
        mail_start_time = context.mail_start_time
    except AttributeError:
        raise Exception(
            'Missing "mail_start_time" context variable. Assign it in a step before'
        )

    host_context = getattr(context.instances, instance)
    mails = host_context.remote_sysutils.get_mails(since=mail_start_time)
    assert len(mails) == 1, f'Invalid mail count: {len(mails)}'
    assert content in mails[0]['body']


@step('I execute "{command}" command on "{instance}"')
def when_i_execute_command_on_instance(context, command, instance):
    host_context = getattr(context.instances, instance)
    host_context.remote_sysutils.send_command(command.split())


@then('I wait until services are ready on "{instance}"')
def then_i_wait_until_services_are_ready_on_instance(context, instance):
    context = getattr(context.instances, instance)
    context.confd_client.status()

    # NOTE: For HA, this check is enough, but feel free to add more services
    def confd_is_ready():
        status = context.confd_client.status()
        assert status['rest_api']['status'] == 'ok'
        assert status['master_tenant']['status'] == 'ok'
        assert status['bus_consumer']['status'] == 'ok'
        assert status['service_token']['status'] == 'ok'

    until.assert_(confd_is_ready, timeout=90)


@when('I initialize wazo-sync on "{instance_master}" to "{instance_slave}"')
def when_i_initialize_xivo_sync_on_instance(context, instance_master, instance_slave):
    master_context = getattr(context.instances, instance_master)
    slave_context = getattr(context.instances, instance_slave)
    password = slave_context.wazo_config['system_password']
    if not password:
        raise Exception('Missing "system_password" configuration')
    command = ['sshpass', '-p', password, 'wazo-sync', '-i']
    master_context.remote_sysutils.send_command(command)
