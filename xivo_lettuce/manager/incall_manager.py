# -*- coding: utf-8 -*-

from lettuce.registry import world
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException
from webservices.webservices import WebServicesFactory
from xivo_lettuce.common import *

INCALL_URL = '/service/ipbx/index.php/call_management/incall/%s'
WS = WebServicesFactory('ipbx/call_management/incall')


def open_add_incall_url():
    URL = INCALL_URL % '?act=add'
    world.browser.get('%s%s' % (world.url, URL))
    world.browser.find_element_by_id('it-incall-exten', 'Incall form not loaded')


def open_list_incall_url():
    URL = INCALL_URL % ('?act=list')
    world.browser.get('%s%s' % (world.url, URL))
    world.browser.find_element_by_id('table-main-listing', 'Incall list not loaded')


def type_incall_did(incall_did):
    world.browser.find_element_by_id('it-incall-exten', 'Incall form not loaded')
    world.incall_did = incall_did
    input_did = world.browser.find_element_by_id('it-incall-exten')
    input_did.send_keys(incall_did)


def remove_incall_with_did(incall_did):
    open_list_incall_url()
    try:
        remove_line(incall_did)
    except NoSuchElementException:
        pass


def incall_is_saved(incall_did):
    open_list_incall_url()
    try:
        incall = find_line(incall_did)
        return incall is not None
    except NoSuchElementException:
        return False
