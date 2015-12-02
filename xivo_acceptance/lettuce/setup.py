# -*- coding: utf-8 -*-

# Copyright (C) 2015 Avencall
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

from lettuce import world

from xivo_acceptance.config import load_config, XivoAcceptanceConfig
from xivo_acceptance.lettuce import debug
from xivo_agentd_client import Client as AgentdClient
from xivo_auth_client import Client as AuthClient
from xivobrowser import XiVOBrowser


def setup_agentd_client():
    world.agentd_client = AgentdClient(world.config['xivo_host'],
                                       token=world.config['auth_token'],
                                       verify_certificate=False)


def setup_auth_token():
    # service_id/service_key is defined in data/assets/xivo-acceptance-key.yml
    auth_client = AuthClient(world.config['xivo_host'],
                             username='xivo-acceptance',
                             password='0b34aefe-5c86-4fda-8a4a-0aac2532d053',
                             verify_certificate=False)
    world.config['auth_token'] = auth_client.token.new('xivo_service', expiration=6*3600)['token']


@debug.logcall
def setup_browser():
    if not world.config['browser']['enable']:
        return

    if hasattr(world, 'display') and hasattr(world, 'browser'):
        _stop_browser()

    from pyvirtualdisplay import Display
    browser_size = width, height = tuple(world.config['browser']['resolution'].split('x', 1))
    world.display = Display(visible=world.config['browser']['visible'], size=browser_size)
    world.display.start()
    world.browser = XiVOBrowser(world.config['debug']['selenium'])
    world.browser.set_window_size(width, height)
    world.timeout = float(world.config['browser']['timeout'])


@debug.logcall
def _stop_browser():
    if not world.config['browser']['enable']:
        return

    world.browser.quit()
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
        world.display.stop()
