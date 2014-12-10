# -*- coding: utf-8 -*-

# Copyright (C) 2013-2014 Avencall
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

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
