# -*- coding: UTF-8 -*-

from lettuce.registry import world
from selenium.webdriver.support.select import Select


def set_select_field_with_label(field_label, value):
    select_input = world.browser.find_element_by_label(field_label)
    Select(select_input).select_by_visible_text(value)


def set_select_field_with_id(field_id, value):
    select_input = world.browser.find_element_by_id(field_id)
    Select(select_input).select_by_visible_text(value)


def set_select_field_with_id_containing(field_id, filter_string):
    select_input = Select(world.browser.find_element_by_id(field_id))
    options = select_input.options
    for option in options:
        if filter_string in option.text:
            select_input.select_by_value(option.get_attribute('value'))
