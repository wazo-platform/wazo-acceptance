# Copyright 2013-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import requests
from behave import given, step, then, when


@given('there are devices with infos')
def given_there_are_devices_with_infos(context):
    context.table.require_columns(['mac'])
    for row in context.table:
        body = row.as_dict()
        plugin_type = body.pop('plugin version', None)
        if plugin_type:
            body['plugin'] = context.helpers.provd.get_latest_plugin_name(plugin_type)

        context.helpers.device.create(body)


@step('the following devices are created via HTTP requests to the provisioning server')
def when_the_following_devices_are_created_via_http_requets_to_the_provisioning_server(context):
    for row in context.table:
        body = row.as_dict()
        body['user_agent'] = body.pop('user-agent')
        context.helpers.provd.create_device_via_http_request(**body)

@then('the following provisioning files are available over HTTPS using secure key "{secure_key}"')
def then_the_following_provisioning_files_are_available_over_https_with_url_key(context, secure_key):
    for row in context.table:
        file_ = row.as_dict()
        url = f"https://{context.wazo_config['wazo_host']}/device/provisioning/{secure_key}/{file_['path']}"
        headers = {
            'User-Agent': file_['user-agent']
        }
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        assert file_['expected_content'] in response.text

@when('I synchronize the device with mac "{mac}"')
def when_i_synchronize_the_device_with_mac(context, mac):
    device = context.helpers.device.get_by(mac=mac)
    context.confd_client.devices.synchronize(device['id'])


@then('the following provisioning files are available over HTTPS')
def then_the_following_provisioning_files_are_available_over_https(context):
    for row in context.table:
        file_ = row.as_dict()
        url = f"https://{context.wazo_config['wazo_host']}/device/provisioning/{file_['path']}"
        headers = {
            'User-Agent': file_['user-agent']
        }
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        assert file_['expected_content'] in response.text
