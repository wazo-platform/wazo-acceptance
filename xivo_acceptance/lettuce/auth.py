# -*- coding: utf-8 -*-

# Copyright 2016 The Wazo Authors  (see the AUTHORS file)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

import logging

from lettuce import world

logger = logging.getLogger('acceptance')
token_renewal_callbacks = []
ONE_HOUR = 3600


def new_auth_token():
    try:
        token_id = world.auth_client.token.new('xivo_service', expiration=6*ONE_HOUR)['token']
    except Exception as e:
        logger.warning('creating auth token failed: %s', e)
        token_id = None
    return token_id


def renew_auth_token():
    token = world.config['auth_token'] = new_auth_token()

    for renewal_callback in token_renewal_callbacks:
        renewal_callback(token)


def register_for_token_renewal(callback):
    '''callbacks signature: my_callback(new_token)'''

    global token_renewal_callbacks
    token_renewal_callbacks.append(callback)
