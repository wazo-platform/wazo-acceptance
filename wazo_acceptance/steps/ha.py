# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from behave import given, when


@given('the HA is enabled as master on "{instance}"')
def given_the_ha_is_enabled_as_master_on_instance(context, instance):
    context = getattr(context.instances, instance)
    context.helpers.ha.set({
        'node_type': 'master',
        'remote_address': context.wazo_config['slave_host']
    })


@given('the HA is enabled as slave on "{instance}"')
def given_the_ha_is_enabled_as_slave(context, instance):
    context = getattr(context.instances, instance)
    context.helpers.ha.set({
        'node_type': 'slave',
        'remote_address': context.wazo_config['master_host']
    })


@when('I disable the HA on "{instance}"')
def when_i_disable_the_ha_on_instance(context, instance):
    context = getattr(context.instances, instance)
    context.helpers.ha.set({
        'node_type': 'disabled',
    })


@when('I enable the HA as master on "{instance}"')
def when_i_enable_the_ha_as_master_on_instance(context, instance):
    context = getattr(context.instances, instance)
    context.helpers.ha.set({
        'node_type': 'master',
        'remote_address': context.wazo_config['slave_host']
    })


@when('I enable the HA as slave on "{instance}"')
def when_i_enable_the_ha_as_slave_on_instance(context, instance):
    context = getattr(context.instances, instance)
    context.helpers.ha.set({
        'node_type': 'slave',
        'remote_address': context.wazo_config['master_host']
    })
