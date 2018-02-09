# -*- coding: utf-8 -*-
# Copyright (C) 2013-2014 Avencall
# Copyright (C) 2016 Proformatique Inc.
# SPDX-License-Identifier: GPL-3.0+

from selenium.common.exceptions import NoSuchElementException
from lettuce import world


class FormErrorException(Exception):
    pass


def submit_form_with_errors(input_id='it-submit'):
    _do_submit(input_id)
    assert_form_errors()


def submit_form(input_id='it-submit'):
    _do_submit(input_id)
    assert_no_form_errors(dump_current_page=True)


def submit_form_ignore_errors(input_id='it-submit'):
    _do_submit(input_id)


def _do_submit(input_id):
    submit_button = world.browser.find_element_by_id(input_id)
    submit_button.click()


def assert_form_errors():
    error_element = _get_form_errors()
    if error_element is None:
        raise Exception('No error occured')


def assert_no_form_errors(dump_current_page=False):
    error_element = _get_form_errors()
    if error_element is not None:
        if dump_current_page:
            world.dump_current_page()
        raise FormErrorException(error_element.text)


def _get_form_errors():
    try:
        return world.browser.find_element_by_id('report-xivo-error', timeout=3)
    except NoSuchElementException:
        pass

    try:
        return world.browser.find_element_by_class_name('fm-txt-error', timeout=1)
    except NoSuchElementException:
        pass

    try:
        return world.browser.find_element_by_class_name('fm-error', timeout=1)
    except NoSuchElementException:
        pass

    return None
