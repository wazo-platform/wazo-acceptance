# -*- coding: utf-8 -*-

import re
import time

from lettuce.registry import world
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By


class MissingTranslationException(Exception):
    pass


class XiVOBrowser(webdriver.Firefox):

    def get(self, url):
        """Get the url and check that there is no missing translation, or raise an exception.
        The missing_translation tag is added in the Webi i18n bbf function."""

        # Get the page
        webdriver.Firefox.get(self, url)

        WebDriverWait(self, world.timeout).until(lambda browser: webdriver.Firefox.page_source)
        source = self.page_source
        # Remove newline, to allow regexp substitution
        source = source.replace('\n', ' ')
        # Remove HTML comments
        source = re.sub('<!--.*-->', '', source)
        source = re.sub('&lt;!--.*--&gt;', '', source)
        # Extract missing translations
        missing_translations = re.finditer("__missing_translation:([^:]*):([^:]*):", source)

        # Format missing translations for output
        missing_translations_list = []
        for missing_translation in missing_translations:
            missing_translations_list.append(missing_translation.group(1) + ":" + missing_translation.group(2))

        # Raise exception if necessary
        if missing_translations_list:
            # Uniquify
            missing_translations_list = sorted(set(missing_translations_list))

            raise MissingTranslationException('\n'.join(missing_translations_list))
        """
        try:
            world.browser.find_element_by_id('page_loaded' % act, '%s %s not loaded' % (module, act))
        except ElementNotVisibleException:
            pass
        """

    def find_element(self, by=By.ID, value=None, message='', timeout=None):
        """This function is called by all find_element_by_*().
           This implementation adds a timeout to search for Webelements."""
        # Do not call lambda browser : browser.find_element -> infinite recursion
        if timeout is None:
            timeout = world.timeout

        try:
            WebDriverWait(self, timeout).until(
                lambda browser: webdriver.Firefox.find_element(self, by, value))
        except TimeoutException:
            raise NoSuchElementException('%s: %s' % (value, message))

        element = webdriver.Firefox.find_element(self, by, value)

        try:
            WebDriverWait(self, timeout).until(
                lambda browser: webdriver.Firefox.find_element(self, by, value).is_displayed())
        except TimeoutException:
            raise ElementNotVisibleException('%s: %s' % (value, message))

        return element

    def find_element_by_id(self, id, message='', timeout=None):
        return self.find_element(By.ID, id, message, timeout)

    def find_element_by_name(self, name, message='', timeout=None):
        return self.find_element(By.NAME, name, message, timeout)

    def find_element_by_xpath(self, xpath, message='', timeout=None):
        return self.find_element(By.XPATH, xpath, message, timeout)

    def find_elements(self, by=By.ID, value=None, message='', timeout=None):
        """This function is called by all find_element_by_*().
           This implementation adds a timeout to search for Webelements."""
        # Do not call lambda browser : browser.find_element -> infinite recursion
        if timeout is None:
            timeout = world.timeout

        try:
            WebDriverWait(self, timeout).until(
                lambda browser: webdriver.Firefox.find_elements(self, by, value))
        except TimeoutException:
            raise NoSuchElementException('%s: %s' % (value, message))

        return webdriver.Firefox.find_elements(self, by, value)

    def find_elements_by_xpath(self, xpath, message='', timeout=None):
        return self.find_elements(By.XPATH, xpath, message, timeout)

    def find_element_by_label(self, label):
        """Finds the first element corresponding to the label containing the argument."""
        webelement_label = self.find_element_by_xpath(
            "//label[text() = '%s' or text() = '%s:']" % (label, label))
        webelement_id = webelement_label.get_attribute('for')
        webelement = self.find_element_by_id(webelement_id)
        return webelement

    def find_elements_by_label(self, label):
        """Finds all elements corresponding to the labels containing the argument."""
        webelement_labels = self.find_elements_by_xpath(
            "//label[text() = '%s' or text() = '%s:']" % (label, label))
        ret = []
        for webelement_label in webelement_labels:
            webelement_id = webelement_label.get_attribute('for')
            ret += self.find_elements_by_id(webelement_id)
        return ret

    def switch_to_alert(self, message='No alert', timeout=5):
        """Adds wait time for alert."""
        count = 0
        while count < timeout:
            alert = webdriver.Firefox.switch_to_alert(self)
            time.sleep(1)
            if alert:
                return alert
            count += 1
        raise Exception(message)
