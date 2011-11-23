# -*- coding: utf-8 -*-

from lettuce.decorators import step
from lettuce.registry import world
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotVisibleException

PG_URL = '/xivo/configuration/index.php/provisioning/general/%s'

def _open_general_url():
    URL = PG_URL % ''
    world.browser.get('%s%s' % (world.url, URL))
    world.wait_for_id('it-submit', 'Provd general configuration page not loaded')

def _type_plugin_server_url(url):
    world.wait_for_name('plugin_server', 'plugin_server form not loaded')
    input_plugin_server = world.browser.find_element_by_name('plugin_server')
    input_plugin_server.clear()
    input_plugin_server.send_keys(url)
    import time
    time.sleep(2)

def update_plugin_server_url(url):
    _open_general_url()
    _type_plugin_server_url(url)
