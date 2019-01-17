# -*- coding: utf-8 -*-
# Copyright (C) 2013-2014 Avencall
# Copyright (C) 2016 Proformatique Inc.
# SPDX-License-Identifier: GPL-3.0-or-later

from lettuce import world


def add_or_replace_trunkcustom(interface):
    delete_trunkcustoms_with_interface(interface)
    add_trunkcustom(interface)


def add_trunkcustom(interface):
    trunk = world.confd_client.trunks.create({})
    endpoint_custom = world.confd_client.endpoints_custom.create({'interface': interface})
    world.confd_client.trunks(trunk).add_endpoint_custom(endpoint_custom)


def delete_trunkcustoms_with_interface(interface):
    endpoints_custom = world.confd_client.endpoints_custom.list(interface=interface)['items']
    for endpoint_custom in endpoints_custom:
        world.confd_client.endpoints_custom.delete(endpoint_custom['id'])
        if endpoint_custom['trunk']:
            world.confd_client.trunks.delete(endpoint_custom['trunk']['id'])
