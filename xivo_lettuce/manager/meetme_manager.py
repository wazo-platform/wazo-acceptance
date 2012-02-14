# -*- coding: utf-8 -*-

from lettuce.registry import world
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException
from webservices.webservices import WebServicesFactory
from xivo_lettuce.common import *


MM_URL = '/service/ipbx/index.php/pbx_settings/meetme/%s'
WS = WebServicesFactory('ipbx/pbx_settings/meetme')


def open_add_form():
    URL = MM_URL % '?act=add'
    world.browser.get('%s%s' % (world.url, URL))
    world.browser.find_element_by_id('it-meetmefeatures-name', 'Meetme add form not loaded')


def open_edit_form(id):
    URL = MM_URL % '?act=edit&id=%d'
    world.browser.get('%s%s' % (world.url, URL % id))
    world.browser.find_element_by_id('it-meetmefeatures-name', 'Meetme edit form not loaded')


def open_list_url():
    URL = MM_URL % '?act=list'
    world.browser.get('%s%s' % (world.url, URL))
    world.browser.find_element_by_id('table-main-listing', 'Meetme list not loaded')


def type_name(name):
    world.browser.find_element_by_id('it-meetmefeatures-name', 'Meetme form not loaded')
    input_name = world.browser.find_element_by_id('it-meetmefeatures-name')
    input_name.clear()
    input_name.send_keys(name)


def type_confno(confno):
    world.browser.find_element_by_id('it-meetmefeatures-confno', 'Meetme form not loaded')
    input_confno = world.browser.find_element_by_id('it-meetmefeatures-confno')
    input_confno.clear()
    input_confno.send_keys(confno)


def type_context(context):
    world.browser.find_element_by_id('it-meetmefeatures-context', 'Meetme form not loaded')
    language_option = world.browser.find_element_by_xpath('//select[@id="it-meetmefeatures-context"]//option[@value="%s"]' % context)
    language_option.click()


def type_maxusers(maxusers):
    world.browser.find_element_by_id('it-meetmefeatures-maxusers', 'Meetme form not loaded')
    input_maxusers = world.browser.find_element_by_id('it-meetmefeatures-maxusers')
    input_maxusers.clear()
    input_maxusers.send_keys(maxusers)


def delete_all_meetme():
    WS.clear()


def is_saved(name):
    open_list_url()
    try:
        meetme = find_line(name)
        return meetme is not None
    except NoSuchElementException:
        return False
