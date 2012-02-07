# -*- coding: utf-8 -*-

from lettuce.registry import world

from selenium.common.exceptions import NoSuchElementException

LINE_URL = '/service/ipbx/index.php/pbx_settings/lines/%s'


def open_add_line_form():
    URL = LINE_URL % '?act=add'
    world.browser.get('%s%s' % (world.url, URL))
    world.browser.find_element_by_id('it-linefeatures-firstname', 'Line add form not loaded')


def open_edit_line_form(id):
    URL = LINE_URL % '?act=edit&id=%d'
    world.browser.get('%s%s' % (world.url, URL % id))
    world.browser.find_element_by_id('it-linefeatures-firstname', 'Line edit form not loaded')


def open_list_line_url():
    URL = LINE_URL % '?act=list'
    world.browser.get('%s%s' % (world.url, URL))
    world.browser.find_element_by_id('table-main-listing', 'Line list not loaded')
