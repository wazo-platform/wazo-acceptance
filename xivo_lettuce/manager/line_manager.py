# -*- coding: utf-8 -*-

from lettuce.registry import world
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException
from webservices.webservices import WebServicesFactory
from xivo_lettuce.common import *

LINE_URL = '/service/ipbx/index.php/pbx_settings/lines/%s'
WS = WebServicesFactory('ipbx/pbx_settings/lines')


def open_add_line_form(proto):
    URL = LINE_URL % '?act=add&proto=%s' % proto
    world.browser.get('%s%s' % (world.url, URL))
    world.browser.find_element_by_id('it-protocol-context', 'Line form not loaded')


def open_edit_line_form(id):
    URL = LINE_URL % '?act=edit&id=%d'
    world.browser.get('%s%s' % (world.url, URL % id))
    world.browser.find_element_by_id('it-protocol-context', 'Line form not loaded')


def open_list_line_url():
    URL = LINE_URL % '?act=list'
    world.browser.get('%s%s' % (world.url, URL))
    world.browser.find_element_by_id('table-main-listing', 'Line list not loaded')
