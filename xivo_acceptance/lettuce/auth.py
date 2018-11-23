# -*- coding: utf-8 -*-
# Copyright 2016-2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

import logging
import uuid

from lettuce import world

logger = logging.getLogger('acceptance')
token_renewal_callbacks = []
ONE_HOUR = 3600


def new_auth_token():
    try:
        token_data = world.config['token_data'] = world.auth_client.token.new(
            'wazo_user',
            expiration=6*ONE_HOUR,
        )
        token_id = token_data['token']
    except Exception as e:
        logger.warning('creating auth token failed: %s', e)
        token_id = None
    return token_id


def invalid_auth_token():
    return str(uuid.uuid4())


def renew_auth_token():
    token = world.config['auth_token'] = new_auth_token()

    for renewal_callback in token_renewal_callbacks:
        renewal_callback(token)


def register_for_token_renewal(callback):
    '''callbacks signature: my_callback(new_token)'''

    global token_renewal_callbacks
    token_renewal_callbacks.append(callback)
