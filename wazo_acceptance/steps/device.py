# Copyright 2013-2026 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import uuid

import requests
from behave import given, step, then, when


@given('there are devices with infos:')
def given_there_are_devices_with_infos(context):
    context.table.require_columns(['mac'])
    for row in context.table:
        body = row.as_dict()
        plugin_type = body.pop('plugin version', None)
        if plugin_type:
            body['plugin'] = context.helpers.provd.get_latest_plugin_name(plugin_type)

        context.helpers.device.create(body)


@when('I synchronize the device with mac "{mac}"')
def when_i_synchronize_the_device_with_mac(context, mac):
    device = context.helpers.device.get_by(mac=mac)
    context.confd_client.devices.synchronize(device['id'])


@step('the following devices are created via HTTP requests to the provisioning server:')
def step_the_following_devices_are_created_via_http_requests_to_the_provisioning_server(context):
    for row in context.table:
        body = row.as_dict()
        body['user_agent'] = body.pop('user-agent')
        context.helpers.provd.create_device_via_http_request(**body)


@then('the following provisioning files are available over HTTP using port "{port}":')
def then_the_following_provisioning_files_are_available_over_http_using_port(context, port):
    host = context.wazo_config['provd']['provisioning_host']
    base_url = f"http://{host}:{port}"
    _provisioning_files_are_available(context, base_url)


@then('the following provisioning files are available over HTTPS:')
def then_the_following_provisioning_files_are_available_over_https(context):
    host = context.wazo_config['provd']['provisioning_host']
    base_url = f"https://{host}/device/provisioning"
    _provisioning_files_are_available(context, base_url)


@then('the following provisioning files are available over HTTPS using provisioning key "{provisioning_key}":')
def then_the_following_provisioning_files_are_available_over_https_using_key(context, provisioning_key):
    host = context.wazo_config['provd']['provisioning_host']
    base_url = f"https://{host}/device/provisioning/{provisioning_key}"
    _provisioning_files_are_available(context, base_url)


@when('I request {count:d} provisioning files with method "{method}" over HTTPS using an invalid provisioning key')
def when_i_request_provisioning_files_using_an_invalid_key(context, count, method):
    if not hasattr(context, 'invalid_provisioning_key'):
        # unique per run: a key left in a log by a previous run can't hide a leak
        context.invalid_provisioning_key = f'invalidkey-{uuid.uuid4().hex}'
    host = context.wazo_config['provd']['provisioning_host']
    base_url = f"https://{host}/device/provisioning/{context.invalid_provisioning_key}"
    for i in range(count):
        try:
            response = requests.request(method, f"{base_url}/{i:012x}.cfg", verify=False, timeout=5)
        except requests.exceptions.RequestException:
            # the IP address is banned by fail2ban, possibly during this request
            break
        assert response.status_code == 404, f'Unexpected status code {response.status_code} for an invalid key'


def _provisioning_files_are_available(context, base_url):
    for row in context.table:
        file_ = row.as_dict()
        url = f"{base_url}/{file_['path']}"
        headers = {'User-Agent': file_['user-agent']}
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        provd_ip_address = context.helpers.provd.get_default_advertised_ip_address()
        expected_content = file_['expected_content'].replace(
            '{{ provd_ip_address }}',
            provd_ip_address or '<unknown>'
        )
        assert expected_content in response.text, f'Could not find "{expected_content}" in response "{response.text}"'
