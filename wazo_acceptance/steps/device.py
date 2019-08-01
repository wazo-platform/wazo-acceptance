# Copyright 2013-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from behave import then, when


@then('there are no devices with mac "{mac}"')
def then_there_are_no_devices_with_mac(context, mac):
    context.helpers.provd.delete_device_with_mac(mac)


@when('the provisioning server receives the following HTTP requests')
def when_the_provisioning_server_receives_the_following_http_requests(context):
    _provisioning_server_http_requests(context)


def _provisioning_server_http_requests(context):
    for request_data in context.table:
        context.helpers.provd.request_http(request_data['path'], request_data['user-agent'])
