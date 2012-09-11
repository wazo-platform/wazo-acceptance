# -*- coding: utf-8 -*-

from lettuce.registry import world
from xivo_lettuce.common import open_url, go_to_tab


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


def get_value_from_ipbx_infos_tab(var_name):
    go_to_tab('IPBX Infos')
    value_cell = world.browser.find_element_by_xpath(
        "//table"
        "//tr[td[@class = 'td-left' and text() = '%s']]"
        "//td[@class = 'td-right']"
        % var_name)
    return value_cell.text
