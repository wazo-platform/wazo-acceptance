# Copyright 2016-2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import logging

logger = logging.getLogger(__name__)
ONE_HOUR = 3600


def new_auth_token(context):
    try:
        token_id = context.auth_client.token.new(expiration=6 * ONE_HOUR)['token']
    except Exception as e:
        logger.warning('creating auth token failed: %s', e)
        token_id = None

    return token_id


def renew_auth_token(context):
    context.token = new_auth_token(context)

    logger.debug('New token for instance %s', context.wazo_config['wazo_host'])
    context.token_pubsub.publish('new-token-id', context.token)
