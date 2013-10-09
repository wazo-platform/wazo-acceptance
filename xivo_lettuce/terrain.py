# -*- coding: utf-8 -*-

# Copyright (C) 2013 Avencall
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

import execnet
import ConfigParser
import os
import sys
import tempfile
import xivo_ws

from lettuce import before, after, world
from sqlalchemy.exc import OperationalError
from xivobrowser import XiVOBrowser

from xivo_acceptance.helpers import asterisk_helper
from xivo_dao.helpers import config as dao_config
from xivo_dao.helpers import db_manager
from xivo_lettuce.common import webi_login_as_default, webi_logout
from xivo_lettuce.ssh import SSHClient
from xivo_lettuce.ws_utils import WsUtils

_CONFIG_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                            '../config/config.ini'))


@before.all
def xivo_lettuce_before_all():
    print 'Configuring...'
    initialize()


@before.each_scenario
def xivo_lettuce_before_each_scenario(scenario):
    world.voicemailid = None
    world.userid = None
    world.number = None
    world.lineid = None
    if world.browser_enable and _webi_configured():
        _check_webi_login_root()


@after.each_step
def xivo_lettuce_after_each_step(step):
    sys.stdout.flush()


@after.each_scenario
def xivo_lettuce_after_each_scenario(scenario):
    _logout_agents()


@after.all
def xivo_lettuce_after_all(total):
    deinitialize()


def read_config():
    config = ConfigParser.RawConfigParser()
    config_environ = os.getenv('LETTUCE_CONFIG')
    if config_environ and os.path.exists(config_environ):
        config_file = config_environ
    else:
        local_config = '%s.local' % _CONFIG_FILE
        if os.path.exists(local_config):
            config_file = local_config
        else:
            config_file = _CONFIG_FILE
    with open(config_file) as fobj:
        config.readfp(fobj)
    return config


def initialize():
    world.config = read_config()
    world.browser_enable = world.config.getboolean('browser', 'enable')
    world.lazy = _LazyWorldAttributes()
    _setup_dao()
    _setup_xivo_client()
    _setup_login_infos()
    _setup_ssh_client_xivo()
    _setup_ssh_client_callgen()
    _setup_ws()
    if world.browser_enable:
        _setup_browser()
        if _webi_configured():
            webi_login_as_default()
    world.logged_agents = []
    world.dummy_ip_address = '10.99.99.99'


def _setup_browser():
    visible = world.config.getboolean('browser', 'visible')
    timeout = world.config.getint('browser', 'timeout')
    resolution = world.config.get('browser', 'resolution')

    from pyvirtualdisplay import Display
    browser_size = width, height = tuple(resolution.split('x', 1))
    world.display = Display(visible=visible, size=browser_size)
    world.display.start()
    world.browser = XiVOBrowser()
    world.browser.set_window_size(width, height)
    world.timeout = timeout


def _setup_dao():
    hostname = world.config.get('xivo', 'hostname')
    dao_config.DB_URI = 'postgresql://asterisk:proformatique@%s/asterisk' % hostname
    dao_config.XIVO_DB_URI = 'postgresql://xivo:proformatique@%s/xivo' % hostname
    db_manager.reinit()
    try:
        world.asterisk_conn = db_manager._asterisk_engine.connect()
    except OperationalError:
        print 'PGSQL ERROR: could not connect to server'


def _setup_xivo_client():
    world.xc_login_timeout = world.config.getint('xivo_client', 'login_timeout')


def _setup_login_infos():
    world.xivo_url = 'https://%s' % world.config.get('xivo', 'hostname')
    world.login = world.config.get('login_infos', 'login')
    world.password = world.config.get('login_infos', 'password')


def _setup_ssh_client_xivo():
    hostname = world.config.get('xivo', 'hostname')
    login = world.config.get('ssh_infos', 'login')
    world.xivo_host = hostname
    world.xivo_login = login
    world.ssh_client_xivo = SSHClient(hostname, login)


def _setup_ssh_client_callgen():
    hostname = world.config.get('callgen', 'hostname')
    login = world.config.get('callgen', 'login')
    world.callgen_host = hostname
    world.callgen_login = login
    world.ssh_client_callgen = SSHClient(hostname, login)


def _setup_ws():
    hostname = world.config.get('xivo', 'hostname')
    login = world.config.get('webservices_infos', 'login')
    password = world.config.get('webservices_infos', 'password')
    world.ws = xivo_ws.XivoServer(hostname, login, password)

    world.restapi_utils_1_0 = WsUtils('1.0')
    world.restapi_utils_1_1 = WsUtils('1.1')


class _LazyWorldAttributes(object):

    @property
    def execnet_gateway(self):
        try:
            return self._execnet_gateway
        except AttributeError:
            hostname = world.config.get('xivo', 'hostname')
            login = world.config.get('ssh_infos', 'login')
            self._execnet_gateway = execnet.makegateway('ssh=%s@%s' % (login, hostname))
            return self._execnet_gateway


def _webi_configured():
    try:
        command = ['test', '-e', '/var/lib/pf-xivo/configured']
        world.ssh_client_xivo.check_call(command)
    except Exception:
        return False
    else:
        return True


def _logout_agents():
    asterisk_helper.logoff_agents(world.logged_agents)
    world.logged_agents = []


def _check_webi_login_root():
    element = world.browser.find_element_by_xpath('//h1[@id="loginbox"]/span[contains(.,"Login")]/b')
    username = element.text
    if username != "root":
        webi_logout()
        webi_login_as_default()


def deinitialize():
    if world.browser_enable:
        _teardown_browser()


def _teardown_browser():
    world.browser.quit()
    world.display.stop()


@world.absorb
def dump_current_page(filename='lettuce.html'):
    """Use this if you want to debug your test
       Call it with world.dump_current_page()"""
    dump_dir = tempfile.mkdtemp(prefix='lettuce-')
    source_file_name = '%s/lettuce-dump.html' % dump_dir
    with open(source_file_name, 'w') as fobj:
        fobj.write(world.browser.page_source.encode('utf-8'))
    image_file_name = '%s/lettuce-dump.png' % dump_dir
    world.browser.save_screenshot(image_file_name)
    print
    print 'Screenshot dumped in %s' % dump_dir
    print
