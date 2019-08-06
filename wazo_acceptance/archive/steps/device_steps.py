# -*- coding: utf-8 -*-
# Copyright 2013-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from lettuce import step, world
from xivo_acceptance.helpers import device_helper, provd_helper


@step(u'Given I have the following devices:')
def given_i_have_the_following_devices(step):
    for deviceinfo in step.hashes:
        if 'latest plugin of' in deviceinfo:
            deviceinfo = dict(deviceinfo)
            deviceinfo['plugin'] = provd_helper.get_latest_plugin_name(deviceinfo['latest plugin of'])
            del deviceinfo['latest plugin of']
        device = device_helper.add_or_replace_device(deviceinfo)
        world.confd_client.devices.autoprov(device['id'])


@step(u'Given the provisioning server has received the following HTTP requests:')
def given_the_provisioning_server_has_received_the_following_http_requests(step):
    _provisioning_server_http_requests(step)


def _provisioning_server_http_requests(step):
    for request_data in step.hashes:
        provd_helper.request_http(request_data['path'], request_data['user-agent'])
