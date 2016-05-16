# -*- coding: utf-8 -*-

# Copyright (C) 2015-2016 Avencall
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

from xivo_acceptance.config import load_config, XivoAcceptanceConfig
from xivo_acceptance.lettuce import debug
from xivo_agentd_client import Client as AgentdClient
from xivo_auth_client import Client as AuthClient
from xivo_confd_client import Client as ConfdClient
from xivobrowser import XiVOBrowser

logger = logging.getLogger('acceptance')


def setup_agentd_client():
    world.agentd_client = AgentdClient(world.config['xivo_host'],
                                       token=world.config['auth_token'],
                                       verify_certificate=False)


def setup_confd_client():
    world.confd_client = ConfdClient(**world.config['confd'])
    world.confd_client.set_token(world.config.get('auth_token'))


def setup_auth_token():
    auth_client = AuthClient(world.config['xivo_host'],
                             username='xivo-acceptance',
                             password='proformatique',
                             verify_certificate=False)
    try:
        token_id = auth_client.token.new('xivo_service', expiration=6*3600)['token']
    except Exception as e:
        logger.warning('creating auth token failed: %s', e)
        token_id = None
    world.config['auth_token'] = token_id


@debug.logcall
def setup_browser():
    world.browser = XiVOBrowser(world.config['debug']['selenium'])


@debug.logcall
def _stop_browser():
    if not world.config['browser']['enable']:
        return

    world.browser.quit()
    if hasattr(world, 'display'):
        world.display.stop()


def setup_config():
    world.config = load_config()


def setup_consul():
    command = 'cat /var/lib/consul/master_token'.split()
    world.config['consul_token'] = world.ssh_client_xivo.out_call(command).strip()


def setup_logging():
    debug.setup_logging(world.config)


@debug.logcall
def setup_provd():
    world.rest_provd = world.xivo_acceptance_config.rest_provd
    world.provd_client = world.xivo_acceptance_config.provd_client


@debug.logcall
def setup_ssh_client():
    world.ssh_client_xivo = world.xivo_acceptance_config.ssh_client_xivo


def setup_xivo_acceptance_config():
    world.xivo_acceptance_config = XivoAcceptanceConfig(world.config)


@debug.logcall
def setup_ws():
    # Prerequisite:
    # - setup_xivo_acceptance_config
    world.ws = world.xivo_acceptance_config.ws_utils
    world.confd_utils_1_1 = world.xivo_acceptance_config.confd_utils_1_1


@debug.logcall
def teardown_browser():
    if world.config['browser']['enable']:
        world.browser.quit()
        if hasattr(world, 'display'):
            world.display.stop()


def setup_xivo_configured():
    try:
        world.xivo_configured = world.confd_client.wizard.get()['configured']
    except Exception:
        world.xivo_configured = False
