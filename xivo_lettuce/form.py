# -*- coding: utf-8 -*-


from lettuce import world
from xivo_lettuce import common
from selenium.webdriver.support.select import Select


def set_text_field(field_label, value):
    text_input = world.browser.find_element_by_label(field_label)
    text_input.clear()
    text_input.send_keys(value)


def set_select_field(field_label, value):
    select_input = world.browser.find_element_by_label(field_label)
    Select(select_input).select_by_visible_text(value)


def submit_form_with_errors():
    try:
        common.submit_form()
    except common.FormErrorException:
        pass
    else:
        raise Exception('No error occurred')
