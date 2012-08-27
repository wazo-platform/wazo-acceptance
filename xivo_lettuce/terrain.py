# -*- coding: utf-8 -*-

import ConfigParser
import os
import xivo_ws
from lettuce import before, after, world
from xivobrowser import XiVOBrowser
from xivo_lettuce.ssh import SSHClient
from selenium.webdriver import FirefoxProfile


_CONFIG_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                            '../config/config.ini'))


@before.all
def initialize_from_config():
    config = _read_config()
    _setup_browser(config)
    _set_jenkins(config)
    _setup_login_infos(config)
    _setup_ssh_client_xivo(config)
    _setup_ssh_client_callgen(config)
    _setup_ws(config)


def _read_config():
    config = ConfigParser.RawConfigParser()
    local_config = '%s.local' % _CONFIG_FILE
    if os.path.exists(local_config):
        config_file = local_config
    else:
        config_file = _CONFIG_FILE
    with open(config_file) as fobj:
        config.readfp(fobj)
    return config


def _setup_browser(config):
    visible = config.getboolean('browser', 'visible')
    timeout = config.getint('browser', 'timeout')

    from pyvirtualdisplay import Display
    profile = _setup_browser_profile()
    world.display = Display(visible=visible, size=(1024, 768))
    world.display.start()
    world.browser = XiVOBrowser(firefox_profile=profile)
    world.timeout = timeout
    world.stocked_infos = {}


def _set_jenkins(config):
    world.jenkins_host = config.get('jenkins', 'hostname')


def _setup_login_infos(config):
    world.host = 'http://%s/' % config.get('xivo', 'hostname')
    world.login = config.get('login_infos', 'login')
    world.password = config.get('login_infos', 'password')
    world.logged = False


def _setup_ssh_client_xivo(config):
    hostname = config.get('xivo', 'hostname')
    login = config.get('ssh_infos', 'login')
    world.xivo_host = hostname
    world.ssh_client_xivo = SSHClient(hostname, login)


def _setup_ssh_client_callgen(config):
    hostname = config.get('callgen', 'hostname')
    login = config.get('ssh_infos', 'login')
    world.callgen_host = hostname
    world.ssh_client_callgen = SSHClient(hostname, login)


def _setup_ws(config):
    hostname = config.get('xivo', 'hostname')
    login = config.get('webservices_infos', 'login')
    password = config.get('webservices_infos', 'password')
    world.ws = xivo_ws.XivoServer(hostname, login, password)


def _setup_browser_profile():
    fp = FirefoxProfile()

    fp.set_preference("browser.download.folderList", 2)
    fp.set_preference("browser.download.manager.showWhenStarting", False)
    fp.set_preference("browser.download.dir", "/tmp/")
    fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/force-download")

    return fp


@world.absorb
def dump_current_page(filename='/tmp/lettuce.html'):
    """Use this if you want to debug your test
       Call it with world.dump_current_page()"""
    with open(filename, 'w') as fobj:
        fobj.write(world.browser.page_source.encode('utf-8'))
    world.browser.save_screenshot(filename + '.png')


@after.all
def teardown_browser(total):
    world.browser.quit()
    world.display.stop()
