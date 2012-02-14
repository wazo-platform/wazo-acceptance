# -*- coding: utf-8 -*-

from lettuce.registry import world
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException
from webservices.webservices import WebServicesFactory
from xivo_lettuce.common import *

TRUNKSIP_URL = '/service/ipbx/index.php/trunk_management/sip/%s'
WSTS = WebServicesFactory('ipbx/trunk_management/sip')


def open_add_trunksip_url():
    URL = TRUNKSIP_URL % '?act=add'
    world.browser.get('%s%s' % (world.url, URL))


def open_list_trunksip_url():
    URL = TRUNKSIP_URL % ('?act=list')
    world.browser.get('%s%s' % (world.url, URL))

