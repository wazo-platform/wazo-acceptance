# -*- coding: utf-8 -*-
# Copyright (C) 2013-2014 Avencall
# SPDX-License-Identifier: GPL-3.0+

from lettuce import world


class Checkbox(object):
    '''Wraps checkboxes from Selenium WebElement, to make them easier to manipulate'''
    def __init__(self, webelement):
        assert(webelement.get_attribute('type') == 'checkbox')
        self.webelement = webelement

    def is_checked(self):
        return self.webelement.is_selected()

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


def set_checkbox_with_id(element_id, checked):
    Checkbox.from_id(element_id).set_checked(checked)
