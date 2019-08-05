# Copyright 2013-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from behave import when


@when('the following devices are created via HTTP requests to the provisioning server')
def when_the_following_devices_are_created_via_http_requets_to_the_provisioning_server(context):
    for request_data in context.table:
        context.helpers.provd.create_device_via_http_request(
            request_data['mac'],
            request_data['path'],
            request_data['user-agent'],
        )
