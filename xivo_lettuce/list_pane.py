# -*- coding: utf-8 -*-

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

    def remove(self, label):
        label = label.replace('"', '\"')
        selector = 'ul.selected li[title="%s"] a' % label
        self.find_and_click(selector)

    def add_all(self):
        selector = 'div.available a.add-all'
        self.find_and_click(selector)

    def remove_all(self):
        selector = 'div.selected a.remove-all'
        self.find_and_click(selector)

