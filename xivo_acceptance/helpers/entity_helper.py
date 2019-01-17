# -*- coding: utf-8 -*-
# Copyright 2013-2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals

from xivo_acceptance.lettuce import auth
from requests.exceptions import HTTPError
from lettuce import world


def add_entity(name, display_name):
    entity = get_entity_with_name(name)
    if not entity:
        tenant = world.auth_client.tenants.new(name=name)
        # Remove the renew_auth_token call when we stop using xivo_admin auth backends
        auth.renew_auth_token()  # The new tenant uuid is not on our token metadata
        body = {'name': name, 'display_name': display_name, 'tenant_uuid': tenant['uuid']}
        world.confd_client.entities.create(body)


def get_default_entity():
    return get_entity(default_entity_id())


def get_entity(id_):
    auth.renew_auth_token()
    return world.confd_client.entities.get(id_)


def get_entity_with_name(name):
    auth.renew_auth_token()
    try:
        entities = world.confd_client.entities.list(name=name)['items']
        for entity in entities:
            return entity
    except HTTPError:
        return None


def default_entity_id():
    default_entity_name = world.config['default_entity']
    default_entity = get_entity_with_name(default_entity_name)
    if not default_entity:
        raise Exception('Invalid default entity {}'.format(default_entity_name))
    return default_entity['id']
