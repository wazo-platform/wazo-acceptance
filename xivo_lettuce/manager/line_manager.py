# -*- coding: utf-8 -*-

from lettuce.registry import world
from xivo_lettuce.common import open_url


def search_line_number(line_number):
    open_url('line')
    searchbox_id = 'it-toolbar-search'
    text_input = world.browser.find_element_by_id(searchbox_id)
    text_input.clear()
    text_input.send_keys(line_number)
    submit_button = world.browser.find_element_by_id('it-toolbar-subsearch')
    submit_button.click()


def unsearch_line():
    open_url('line')
    searchbox_id = 'it-toolbar-search'
    text_input = world.browser.find_element_by_id(searchbox_id)
    text_input.clear()
    submit_button = world.browser.find_element_by_id('it-toolbar-subsearch')
    submit_button.click()
