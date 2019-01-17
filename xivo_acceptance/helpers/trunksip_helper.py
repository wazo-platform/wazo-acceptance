# -*- coding: utf-8 -*-
# Copyright (C) 2013-2014 Avencall
# Copyright (C) 2016 Proformatique Inc.
# SPDX-License-Identifier: GPL-3.0-or-later

from lettuce import world


def add_trunksip(host, name, context='default', type='friend'):
    body = {'username': name,
            'secret': name,
            'host': host,
            'type': type}
    endpoint_sip = world.confd_client.endpoints_sip.create(body)

    body = {'context': context}
    trunk = world.confd_client.trunks.create(body)

    world.confd_client.trunks(trunk).add_endpoint_sip(endpoint_sip)


def add_or_replace_trunksip(host, name, context='default', type='friend'):
    delete_trunksips_with_name(name)
    add_trunksip(host, name, context, type)


def delete_trunksips_with_name(name):
    endpoints_sip = world.confd_client.endpoints_sip.list(username=name)['items']
    for endpoint_sip in endpoints_sip:
        world.confd_client.endpoints_sip.delete(endpoint_sip['id'])
        if endpoint_sip['trunk']:
            world.confd_client.trunks.delete(endpoint_sip['trunk']['id'])


def find_trunksip_id_with_name(name):
    endpoints_sip = world.confd_client.endpoints_sip.list(username=name)['items']
    if len(endpoints_sip) != 1:
        raise Exception('expecting 1 sip trunk with name %r; found %s' %
                        (name, len(endpoints_sip)))
    return endpoints_sip[0]['trunk']['id']
