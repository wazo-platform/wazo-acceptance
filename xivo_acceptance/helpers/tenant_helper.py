# -*- coding: utf-8 -*-
# Copyright 2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from lettuce import world


def get_tenant_uuid(name=None):
    name = name or world.config['default_entity']
    tenants = world.auth_client.tenants.list(name=name)['items']
    for tenant in tenants:
        if tenant['name'] != name:
            continue
        return tenant['uuid']
