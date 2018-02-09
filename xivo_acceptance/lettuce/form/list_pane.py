# -*- coding: utf-8 -*-
# Copyright 2013-2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

import time

from lettuce import world


class ListPane(object):
    '''Wraps a jQuery Multiselect to make it easier to manipulate through Selenium'''

    def __init__(self, webelement):
        self.pane = webelement.find_element_by_css_selector(".ui-multiselect")
        self.pane_search = self.pane.find_element_by_css_selector(".search")

    def find_and_click(self, selector, label=None):
        element = self.pane.find_element_by_css_selector(selector)
        if label:
            # To fix https://bugzilla.mozilla.org/show_bug.cgi?id=1295538
            self.pane_search.send_keys(label)
            time.sleep(0.2)
        element.click()
        self.pane_search.clear()

    def add(self, label):
        label = label.replace('"', '\"')
        selector = 'ul.available li[title="%s"] a' % label
        self.find_and_click(selector, label)

    def add_contains(self, label):
        label = label.replace('"', '\"')
        selector = 'ul.available li[title*="%s"] a' % label
        self.find_and_click(selector, label)

    def remove(self, label):
        label = label.replace('"', '\"')
        selector = 'ul.selected li[title="%s"] a' % label
        self.find_and_click(selector)

    def remove_contains(self, label):
        label = label.replace('"', '\"')
        selector = 'ul.selected li[title*="%s"] a' % label
        self.find_and_click(selector)

    def add_all(self):
        selector = 'div.available a.add-all'
        self.find_and_click(selector)

    def remove_all(self):
        selector = 'div.selected a.remove-all'
        self.find_and_click(selector)

    def available_labels(self):
        selector = 'div.available .ui-element'
        return self._labels_by_selector(selector)

    def selected_labels(self):
        selector = 'div.selected .ui-element'
        return self._labels_by_selector(selector)

    def _labels_by_selector(self, css_selector):
        elements = self.pane.find_elements_by_css_selector(css_selector)
        return [element.get_attribute('title') for element in elements]

    @classmethod
    def from_id(cls, webelement_id):
        webelement = world.browser.find_element_by_id(webelement_id)
        return cls(webelement)
