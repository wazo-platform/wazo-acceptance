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
ONE_HOUR = 3600

def update_auth_token():
    try:
        token_id = world.auth_client.token.new('xivo_service', expiration=6*ONE_HOUR)['token']
    except Exception as e:
        logger.warning('creating auth token failed: %s', e)
        token_id = None
    world.config['auth_token'] = token_id


def update_auth_token_and_clients():
    update_auth_token()
    world.agentd_client.set_token(world.config['auth_token'])
    world.confd_client.set_token(world.config['auth_token'])
    world.ctid_ng_client.set_token(world.config['auth_token'])
    world.dird_client.set_token(world.config['auth_token'])
