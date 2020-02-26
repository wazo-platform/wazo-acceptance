# Copyright 2019-2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import random
import string

from behave import given, when, then

from wazo_acceptance import auth


def random_string(length, sample=string.ascii_lowercase):
    return ''.join(random.choice(sample) for _ in range(length))


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
        'password': random_string(10, sample=string.printable),
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


@then('there is a user "{username}" on "{instance}"')
def then_there_is_a_user_username_on_instance(context, username, instance):
    context = getattr(context.instances, instance)
    assert context.helpers.user.get_by(username=username)
