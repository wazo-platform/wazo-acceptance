# -*- coding: utf-8 -*-

from lettuce.registry import world
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException
from webservices.webservices import WebServicesFactory
from xivo_lettuce.common import *

OUTCALL_URL = '/service/ipbx/index.php/call_management/outcall/%s'
WS = WebServicesFactory('ipbx/call_management/outcall')


def open_add_outcall_url():
    URL = OUTCALL_URL % '?act=add'
    world.browser.get('%s%s' % (world.url, URL))


def open_list_outcall_url():
    URL = OUTCALL_URL % ('?act=list')
    world.browser.get('%s%s' % (world.url, URL))


def exten_line(exten):
    """Find the line of an outcall exten in the list of an outcall extens."""
    return world.browser.find_element_by_xpath(
        "//table[@id='list_exten']//tr[.//input[@name='dialpattern[exten][]' and @value='%s']]" % exten)
