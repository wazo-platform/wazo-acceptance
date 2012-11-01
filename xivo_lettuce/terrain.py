# -*- coding: utf-8 -*-

import ConfigParser
import os
import xivo_ws
from lettuce import before, after, world
from xivobrowser import XiVOBrowser
from xivo_lettuce.ssh import SSHClient
from selenium.webdriver import FirefoxProfile
from xivo_lettuce.common import webi_login_as_default, go_to_home_page
from xivo_lettuce.manager import asterisk_manager


_CONFIG_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                            '../config/config.ini'))


@before.all
def xivo_lettuce_before_all():
    initialize()


@after.each_scenario
def xivo_lettuce_after_each(scenario):
    _logout_agents()


@after.all
def xivo_lettuce_after_all(total):
    deinitialize()


def initialize():
    config = read_config()
    _setup_browser(config)
    _setup_xivo_client(config)
    _setup_login_infos(config)
    _setup_ssh_client_xivo(config)
    _setup_ssh_client_callgen(config)
    _setup_ws(config)
    if _webi_configured():
        _log_on_webi()
    world.logged_agents = []


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


def _setup_browser_profile():
    fp = FirefoxProfile()

    fp.set_preference("browser.download.folderList", 2)
    fp.set_preference("browser.download.manager.showWhenStarting", False)
    fp.set_preference("browser.download.dir", "/tmp/")
    fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/force-download")

    return fp


def _setup_xivo_client(config):
    world.xc_login_timeout = config.getint('xivo_client', 'login_timeout')


def _setup_login_infos(config):
    world.host = 'http://%s/' % config.get('xivo', 'hostname')
    world.login = config.get('login_infos', 'login')
    world.password = config.get('login_infos', 'password')
    world.logged = False


def _setup_ssh_client_xivo(config):
    hostname = config.get('xivo', 'hostname')
    login = config.get('ssh_infos', 'login')
    world.xivo_host = hostname
    world.xivo_login = login
    world.ssh_client_xivo = SSHClient(hostname, login)
    return world.ssh_client_xivo


def _setup_ssh_client_callgen(config):
    hostname = config.get('callgen', 'hostname')
    login = config.get('callgen', 'login')
    world.callgen_host = hostname
    world.callgen_login = login
    world.ssh_client_callgen = SSHClient(hostname, login)


def _setup_ws(config):
    hostname = config.get('xivo', 'hostname')
    login = config.get('webservices_infos', 'login')
    password = config.get('webservices_infos', 'password')
    world.ws = xivo_ws.XivoServer(hostname, login, password)
    return world.ws


def _webi_configured():
    try:
        command = ['test', '-e', '/etc/pf-xivo/web-interface/xivo.ini']
        world.ssh_client_xivo.check_call(command)
    except Exception:
        return False
    else:
        return True


def _log_on_webi():
    go_to_home_page()
    webi_login_as_default()


def _logout_agents():
    asterisk_manager.logoff_agents(world.logged_agents)
    world.logged_agents = []


def deinitialize():
    _teardown_browser()


def _teardown_browser():
    world.browser.quit()
    world.display.stop()


@world.absorb
def dump_current_page(filename='/tmp/lettuce.html'):
    """Use this if you want to debug your test
       Call it with world.dump_current_page()"""
    with open(filename, 'w') as fobj:
        fobj.write(world.browser.page_source.encode('utf-8'))
    world.browser.save_screenshot(filename + '.png')
