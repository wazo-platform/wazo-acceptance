# -*- coding: utf-8 -*-

from selenium.common.exceptions import NoSuchElementException
from lettuce import world


class FormErrorException(Exception):
    pass


def submit_form_with_errors():
    try:
        submit_form()
    except FormErrorException:
        pass
    else:
        raise Exception('No error occurred')


def submit_form(input_id='it-submit'):
    submit_button = world.browser.find_element_by_id(input_id)
    submit_button.click()
    try:
        error_element = find_form_errors()
    except NoSuchElementException:
        pass
    else:
        raise FormErrorException(error_element.text)


def assert_form_errors():
    assert find_form_errors() is not None


def find_form_errors():
    return world.browser.find_element_by_id('report-xivo-error')
