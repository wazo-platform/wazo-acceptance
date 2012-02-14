# -*- coding: utf-8 -*-

from lettuce.registry import world
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException
from webservices.webservices import WebServicesFactory
from xivo_lettuce.common import *


IAXGENERAL_URL = '/service/ipbx/index.php/general_settings/iax/'
WSTS = WebServicesFactory('ipbx/general_settings/iax')


def open_general_iax_url():
    world.browser.get('%s%s' % (world.url, IAXGENERAL_URL))


def find_call_limit_line(destination=None, netmask=None, limit=None):
    xpath = _xpath_call_limit_line(destination, netmask, limit)
    line = world.browser.find_element_by_xpath(xpath)
    return line


def find_call_limit_lines(destination=None, netmask=None, limit=None):
    xpath = _xpath_call_limit_line(destination, netmask, limit)
    lines = world.browser.find_elements_by_xpath(xpath)
    return lines


def _xpath_call_limit_line(destination=None, netmask=None, limit=None):
    xpath = "//tbody[@id='disp']/tr"
    filters = []
    if destination is not None:
        filters.append("td/input[@name='calllimits[destination][]' "
                                 "and @value='%s']" % destination)
    if netmask is not None:
        filters.append("td/input[@name='calllimits[netmask][]' "
                                 "and @value='%s']" % netmask)
    if limit is not None:
        filters.append("td/input[@name='calllimits[calllimits][]' "
                                 "and @value='%s']" % limit)
    if len(filters) > 0:
        xpath += "[" + ' and '.join(filters) + "]"
    return xpath
