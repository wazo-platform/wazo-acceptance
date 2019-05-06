# -*- coding: utf-8 -*-
# Copyright 2013-2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from lettuce import world


def add_trunkiax(name, context='default'):
    endpoint = world.confd_client.endpoints_iax.create({'name': name})
    trunk = world.confd_client.trunks.create({'context': context})
    world.confd_client.trunks(trunk).add_endpoint_iax(endpoint)


def add_or_replace_trunkiax(name, context='default'):
    delete_trunkiaxs_with_name(name)
    add_trunkiax(name, context)


def delete_trunkiaxs_with_name(name):
    endpoints = world.confd_client.endpoints_iax.list(name=name)['items']
    for endpoint in endpoints:
        world.confd_client.endpoints_iax.delete(endpoint)
        if endpoint['trunk']:
            world.confd_client.trunks.delete(endpoint['trunk']['id'])
