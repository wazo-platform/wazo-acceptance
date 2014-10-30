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

from lettuce import world


class ListPane(object):
    '''Wraps a jQuery Multiselect to make it easier to manipulate through Selenium'''

    def __init__(self, webelement):
        self.pane = webelement.find_element_by_css_selector(".ui-multiselect")

    def find_and_click(self, selector):
        element = self.pane.find_element_by_css_selector(selector)
        element.click()

    def add(self, label):
        label = label.replace('"', '\"')
        selector = 'ul.available li[title="%s"] a' % label
        self.find_and_click(selector)

    def add_contains(self, label):
        label = label.replace('"', '\"')
        selector = 'ul.available li[title*="%s"] a' % label
        self.find_and_click(selector)

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
