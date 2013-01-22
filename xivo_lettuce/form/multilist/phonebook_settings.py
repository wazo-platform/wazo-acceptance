# -*- coding: utf-8 -*-

# Copyright (C) 2013 Avencall
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

from lettuce import world
from selenium.common.exceptions import NoSuchElementException


class PhonebookSettingsMultilist(object):
    'Wraps the "multilist" widget found on the IPBX / General settings / Phonebook page'

    def __init__(self, multilist_element):
        self._button_add = multilist_element.find_element_by_xpath('./div/div/a[1]')
        self._button_del = multilist_element.find_element_by_xpath('./div/div/a[2]')
        self._select = multilist_element.find_element_by_xpath('.//select')

    def add(self, value):
        self._button_add.click()
        alert = world.browser.switch_to_alert()
        alert.send_keys(value)
        alert.accept()

    def remove_all(self):
        while True:
            option = self._get_first_option()
            if option is None:
                break
            option.click()
            self._button_del.click()

    def _get_first_option(self):
        try:
            return self._select.find_element_by_xpath('./option[1]')
        except NoSuchElementException:
            return None

    @classmethod
    def from_id(cls, multilist_id):
        multilist_element = world.browser.find_element_by_id(multilist_id)
        return cls(multilist_element)
