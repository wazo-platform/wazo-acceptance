# -*- coding: utf-8 -*-

from lettuce.registry import world
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException
from webservices.webservices import WebServicesFactory
from xivo_lettuce.common import *


TRUNKIAX_URL = '/service/ipbx/index.php/trunk_management/iax/%s'
WS = WebServicesFactory('ipbx/trunk_management/iax')


def open_add_trunkiax_url():
    URL = TRUNKIAX_URL % '?act=add'
    world.browser.get('%s%s' % (world.url, URL))


def open_list_trunkiax_url():
    URL = TRUNKIAX_URL % ('?act=list')
    world.browser.get('%s%s' % (world.url, URL))
