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
    error_element = _do_submit(input_id)
    if not error_element:
        raise Exception('No error occurred')


def submit_form(input_id='it-submit'):
    error_element = _do_submit(input_id)
    if error_element:
        world.dump_current_page()
        raise FormErrorException(error_element.text)


def _do_submit(input_id):
    submit_button = world.browser.find_element_by_id(input_id)
    submit_button.click()

    try:
        error_element = find_form_errors()
    except NoSuchElementException:
        error_element = None

    return error_element


def assert_form_errors():
    assert find_form_errors() is not None


def find_form_errors():
    return world.browser.find_element_by_id('report-xivo-error')
