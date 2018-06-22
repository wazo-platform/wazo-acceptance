# -*- coding: utf-8 -*-
# Copyright 2013-2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

import logging

from lettuce import world

logger = logging.getLogger(__name__)


def add_or_replace_outcall(data):
    delete_outcalls_with_name(data['name'])
    add_outcall(data)


def add_outcall(data):
    outcall = world.confd_client.outcalls.create({'name': data['name']})
    logger.critical('adding extensions')
    logger.critical('tenant id: %s', world.confd_client._tenant_id)
    logger.critical('default_tenant: %s', world.confd_client._default_tenant_id)
    logger.critical('token: %s', world.confd_client._token_id)
    for extension in data.get('extensions', []):
        extension_confd = world.confd_client.extensions.create({'exten': extension['exten'],
                                                                'context': extension['context']})
        world.confd_client.outcalls(outcall['id']).add_extension(extension_confd,
                                                                 strip_digits=int(extension['stripnum']),
                                                                 caller_id=extension['caller_id'])
    world.confd_client.outcalls(outcall['id']).update_trunks(data['trunks'])


def delete_outcalls_with_name(name):
    outcalls = world.confd_client.outcalls.list(name=name)['items']
    for outcall in outcalls:
        _delete_outcall(outcall)


def delete_outcalls_with_context(context):
    outcalls = world.confd_client.outcalls.list()['items']
    for outcall in outcalls:
        for extension in outcall['extensions']:
            if extension['context'] == context:
                _delete_outcall(outcall)
                break


def _delete_outcall(outcall):
    world.confd_client.outcalls.delete(outcall['id'])
    for extension in outcall['extensions']:
        world.confd_client.extensions.delete(extension['id'])
