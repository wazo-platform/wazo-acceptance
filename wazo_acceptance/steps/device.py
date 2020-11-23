# Copyright 2013-2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from behave import given, step, when


@given('there are devices with infos')
def given_there_are_devices_with_infos(context):
    context.table.require_columns(['mac'])
    for row in context.table:
        body = row.as_dict()
        plugin_type = body.pop('latest plugin of', None)
        if plugin_type:
            body['plugin'] = context.helpers.provd.get_latest_plugin_name(plugin_type)

        context.helpers.device.create(body)


@step('the following devices are created via HTTP requests to the provisioning server')
def when_the_following_devices_are_created_via_http_requets_to_the_provisioning_server(context):
    for row in context.table:
        body = row.as_dict()
        body['user_agent'] = body.pop('user-agent')
        context.helpers.provd.create_device_via_http_request(**body)


@when('I synchronize the device with mac "{mac}"')
def when_i_synchronize_the_device_with_mac(context, mac):
    device = context.helpers.device.get_by(mac=mac)
    context.confd_client.devices.synchronize(device['id'])
