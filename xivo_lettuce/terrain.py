# -*- coding: utf-8 -*-

import ConfigParser
import os
from lettuce import before, after, world
from xivobrowser import XiVOBrowser
from xivo_lettuce.ssh import SSHClient


_CONFIG_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                            '../config/config.ini'))


@before.all
def setup_browser():
    from pyvirtualdisplay import Display
    world.display = Display(visible=1, size=(1024, 768))
    world.display.start()
    world.browser = XiVOBrowser()
    world.timeout = 1
    world.stocked_infos = {}


@before.all
def initialize_from_config():
    config = _read_config()
    _setup_login_infos(config)
    _setup_ssh_client(config)


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


def _setup_login_infos(config):
    world.login = config.get('login_infos', 'login')
    world.password = config.get('login_infos', 'password')
    world.host = config.get('login_infos', 'host')
    world.logged = False


def _setup_ssh_client(config):
    hostname = config.get('ssh_infos', 'hostname')
    login = config.get('ssh_infos', 'login')
    world.ssh_client = SSHClient(hostname, login)


@world.absorb
def dump_current_page(filename='/tmp/lettuce.html'):
    """Use this if you want to debug your test
       Call it with world.dump_current_page()"""
    f = open(filename, 'w')
    f.write(world.browser.page_source.encode('utf-8'))
    f.close()
    world.browser.save_screenshot(filename + '.png')


@after.all
def teardown_browser(total):
    world.browser.quit()
    world.display.stop()
