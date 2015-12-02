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
from xivobrowser import XiVOBrowser


@debug.logcall
def setup_browser():
    # Prerequisite:
    # - setup_config
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


def setup_logging():
    # Prerequisite:
    # - setup_config
    debug.setup_logging(world.config)


@debug.logcall
def setup_ssh_client():
    # Prerequisite:
    # - setup_xivo_acceptance_config
    world.ssh_client_xivo = world.xivo_acceptance_config.ssh_client_xivo


def setup_xivo_acceptance_config():
    # Prerequisite:
    # - setup_config
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
