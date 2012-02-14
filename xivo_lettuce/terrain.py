# -*- coding: utf-8 -*-

import ConfigParser
import os
from lettuce import before, after, world
from xivobrowser import XiVOBrowser


_CONFIG_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), 
                                            '../config/config.ini'))


@before.all
def setup_browser():
    from pyvirtualdisplay import Display
    Display(visible=0, size=(1024, 768)).start()
    world.browser = XiVOBrowser()
    world.timeout = 1
    world.stocked_infos = {}


@before.all
def setup_login_infos():
    _config = ConfigParser.RawConfigParser()
    local_config = '%s.local' % _CONFIG_FILE
    if os.path.exists(local_config):
        config_file = local_config
    elif os.path.exists(_CONFIG_FILE):
        config_file = _CONFIG_FILE
    else:
        raise "config file doesn't exist"
    with open(config_file) as fobj:
        _config.readfp(fobj)
    world.login = _config.get('login_infos', 'login')
    world.password = _config.get('login_infos', 'password')
    world.host = _config.get('login_infos', 'host')
    world.logged = False


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
