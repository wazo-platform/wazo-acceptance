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

import ConfigParser
import os
import tempfile
import xivo_ws
from lettuce import before, after, world
from xivobrowser import XiVOBrowser
from selenium.webdriver import FirefoxProfile
from xivo_dao.helpers import config as dao_config
from xivo_lettuce.common import webi_login_as_default, go_to_home_page, webi_logout
from xivo_lettuce.manager import asterisk_manager
from xivo_lettuce.ssh import SSHClient
from xivo_lettuce.func import st_time

_CONFIG_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                            '../config/config.ini'))


@before.all
def xivo_lettuce_before_all():
    initialize()


@before.each_scenario
def xivo_lettuce_before_each(scenario):
    if world.browser_enable and _webi_configured():
        _check_webi_login_root()


@after.each_scenario
def xivo_lettuce_after_each(scenario):
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
    _setup_dao()
    _setup_xivo_client()
    _setup_login_infos()
    _setup_ssh_client_xivo()
    _setup_ssh_client_callgen()
    _setup_ws()
    if world.browser_enable:
        _setup_browser()
        if _webi_configured():
            _log_on_webi()
    world.logged_agents = []


@st_time
def _setup_browser():
    visible = world.config.getboolean('browser', 'visible')
    timeout = world.config.getint('browser', 'timeout')

    from pyvirtualdisplay import Display
    profile = _setup_browser_profile()
    world.display = Display(visible=visible, size=(1024, 768))
    world.display.start()
    world.browser = XiVOBrowser(firefox_profile=profile)
    world.timeout = timeout
    world.stocked_infos = {}


def _setup_browser_profile():
    fp = FirefoxProfile()

    fp.set_preference("browser.download.folderList", 2)
    fp.set_preference("browser.download.manager.showWhenStarting", False)
    fp.set_preference("browser.download.dir", "/tmp/")
    fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/force-download")

    return fp


def _setup_dao():
    hostname = world.config.get('xivo', 'hostname')
    dao_config.DB_URI = 'postgresql://asterisk:proformatique@%s/asterisk' % hostname


def _setup_xivo_client():
    world.xc_login_timeout = world.config.getint('xivo_client', 'login_timeout')


def _setup_login_infos():
    world.host = 'http://%s/' % world.config.get('xivo', 'hostname')
    world.login = world.config.get('login_infos', 'login')
    world.password = world.config.get('login_infos', 'password')
    world.logged = False


def _setup_ssh_client_xivo():
    hostname = world.config.get('xivo', 'hostname')
    login = world.config.get('ssh_infos', 'login')
    world.xivo_host = hostname
    world.xivo_login = login
    world.ssh_client_xivo = SSHClient(hostname, login)
    return world.ssh_client_xivo


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
    return world.ws


def _webi_configured():
    try:
        command = ['test', '-e', '/var/lib/pf-xivo/configured']
        world.ssh_client_xivo.check_call(command)
    except Exception:
        return False
    else:
        return True


@st_time
def _log_on_webi():
    go_to_home_page()
    webi_login_as_default()


def _logout_agents():
    asterisk_manager.logoff_agents(world.logged_agents)
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
