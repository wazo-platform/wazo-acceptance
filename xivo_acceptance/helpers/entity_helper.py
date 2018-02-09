# -*- coding: utf-8 -*-
# Copyright (C) 2013-2016 Avencall
# SPDX-License-Identifier: GPL-3.0+

from __future__ import unicode_literals

from requests.exceptions import HTTPError
from lettuce import world


def add_entity(name, display_name):
    entity = get_entity_with_name(name)
    if not entity:
        body = {'name': name, 'display_name': display_name}
        world.confd_client.entities.create(body)


def get_entity_with_name(name):
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
