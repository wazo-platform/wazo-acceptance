# -*- coding: utf-8 -*-

from lettuce.registry import world
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException
from webservices.webservices import WebServicesFactory
from xivo_lettuce.common import *


TRUNKCUSTOM_URL = '/service/ipbx/index.php/trunk_management/custom/%s'
WS = WebServicesFactory('ipbx/trunk_management/custom')


def open_add_trunkcustom_url():
    URL = TRUNKCUSTOM_URL % '?act=add'
    world.browser.get('%s%s' % (world.url, URL))


def open_list_trunkcustom_url():
    URL = TRUNKCUSTOM_URL % ('?act=list')
    world.browser.get('%s%s' % (world.url, URL))
