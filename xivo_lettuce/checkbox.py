# -*- coding: utf-8 -*-

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
