# -*- coding: UTF-8 -*-

from lettuce.registry import world
from selenium.webdriver.support.select import Select


def set_select_field_with_label(field_label, value):
    select_input = world.browser.find_element_by_label(field_label)
    Select(select_input).select_by_visible_text(value)


def set_select_field_with_id(field_id, value):
    select_input = world.browser.find_element_by_id(field_id)
    Select(select_input).select_by_visible_text(value)
