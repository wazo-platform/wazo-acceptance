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


class Checkbox(object):
    '''Wraps checkboxes from Selenium WebElement, to make them easier to manipulate'''
    def __init__(self, webelement):
        assert(webelement.get_attribute('type') == 'checkbox')
        self.webelement = webelement

    def is_checked(self):
        return self.webelement.get_attribute('checked') == 'true'

    def set_checked(self, checkstate):
        if self.is_checked() != checkstate:
            self.webelement.click()

    def check(self):
        self.set_checked(True)

    def uncheck(self):
        self.set_checked(False)

    @classmethod
    def from_label(cls, label):
        option_element = world.browser.find_element_by_label(label)
        return cls(option_element)

    @classmethod
    def from_id(cls, id):
        option_element = world.browser.find_element_by_id(id)
        return cls(option_element)

    @classmethod
    def from_value(cls, id):
        option_element = world.browser.find_element_by_id(id)
        return cls(option_element)


def check_checkbox_with_id(element_id):
    Checkbox.from_id(element_id).check()


def uncheck_checkbox_with_id(element_id):
    Checkbox.from_id(element_id).uncheck()
