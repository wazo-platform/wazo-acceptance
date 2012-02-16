# -*- coding: utf-8 -*-

import time
    
from lettuce.registry import world
from xivo_lettuce.common import *


WS = get_webservices('provd_general')


def type_plugin_server_url(url):
    world.browser.find_element_by_name('plugin_server', 'plugin_server form not loaded')
    input_plugin_server = world.browser.find_element_by_name('plugin_server')
    input_plugin_server.clear()
    input_plugin_server.send_keys(url)
    time.sleep(2)


def update_plugin_server_url(url):
    open_url('provd_general')
    type_plugin_server_url(url)
