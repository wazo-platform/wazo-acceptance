# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from behave import when


@when('I enable the DHCP feature')
def when_i_enable_the_dhcp_feature(context):
    context.confd_client.dhcp.update({
        'active': True,
        'pool_start': '192.168.99.1',
        'pool_end': '192.168.99.9',
    })


@when('I disable the DHCP feature')
def when_i_disable_the_dhcp_feature(context):
    context.confd_client.dhcp.update({
        'active': False,
    })
