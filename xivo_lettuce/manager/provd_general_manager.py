# -*- coding: utf-8 -*-

from lettuce.registry import world
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException
from webservices.webservices import WebServicesFactory
from xivo_lettuce.common import *


PG_URL = '/xivo/configuration/index.php/provisioning/general/%s'
WS = WebServicesFactory('configuration/provisioning/general')


def open_general_url():
    URL = PG_URL % ''
    world.browser.get('%s%s' % (world.url, URL))
    world.browser.find_element_by_id('it-submit', 'Provd general configuration page not loaded')


def type_plugin_server_url(url):
    world.browser.find_element_by_name('plugin_server', 'plugin_server form not loaded')
    input_plugin_server = world.browser.find_element_by_name('plugin_server')
    input_plugin_server.clear()
    input_plugin_server.send_keys(url)
    import time
    time.sleep(2)


def update_plugin_server_url(url):
    open_general_url()
    type_plugin_server_url(url)
