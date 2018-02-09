# -*- coding: utf-8 -*-
# Copyright (C) 2013-2014 Avencall
# SPDX-License-Identifier: GPL-3.0+

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
