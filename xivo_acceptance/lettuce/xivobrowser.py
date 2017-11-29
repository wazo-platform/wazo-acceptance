# -*- coding: utf-8 -*-

# Copyright 2013-2017 The Wazo Authors  (see the AUTHORS file)
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

import re
import time

from lettuce.registry import world
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from xivo_acceptance.lettuce import common
from xivo_acceptance.lettuce.exception import MissingTranslationException


class XiVOBrowser(object):

    def __init__(self, debug=False):
        self._debug = debug
        self._instance = None

    def __getattr__(self, name):
        if not self._instance:
            self._start_client()

        return getattr(self._instance, name)

    def quit(self):
        if self._instance:
            self._instance.quit()

        self._instance = None

    def _start_client(self):
        display = world.display.get_instance()
        if world.config['browser'].get('docker', False):
            self._instance = _XiVORemoteBrowserImplementation(self._debug)
        else:
            self._instance = _XiVOLocalBrowserImplementation(self._debug)
        width, height = display.size
        self._instance.set_window_size(width, height)
        world.timeout = float(world.config['browser']['timeout'])

        if world.xivo_configured:
            try:
                element = self._instance.find_element_by_xpath('//h1[@id="loginbox"]/span[contains(.,"Login")]/b')
                username = element.text
            except NoSuchElementException:
                common.webi_login_as_default()
            else:
                if username != "root":
                    common.webi_logout()
                    common.webi_login_as_default()


class _XiVOBrowserMixin(object):

    DOWNLOAD_DIR = '/tmp'

    def _setup_browser_profile(self):
        fp = FirefoxProfile()

        # disable multi-process Firefox that probably causing some crashes
        fp.set_preference('browser.tabs.remote.autostart', False)
        fp.set_preference('browser.tabs.remote.autostart.2', False)

        fp.set_preference("browser.download.folderList", 2)
        fp.set_preference("browser.download.manager.showWhenStarting", False)
        fp.set_preference("browser.download.dir", self.DOWNLOAD_DIR + '/')
        fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/force-download;text/csv")
        fp.set_preference("reader.parse-on-load.enabled", False)

        if self._debug:
            fp.set_preference("webdriver.log.file", "/tmp/firefox_console")

        return fp

    def get(self, url):
        """Get the url and check that there is no missing translation, or raise an exception.
        The missing_translation tag is added in the Webi i18n bbf function."""

        # Get the page
        super(_XiVOBrowserMixin, self).get(url)

        WebDriverWait(self, world.timeout).until(lambda _: super(_XiVOBrowserMixin, self).page_source)
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
                lambda browser: super(_XiVOBrowserMixin, self).find_element(by, value))
        except TimeoutException:
            raise NoSuchElementException('%s: %s' % (value, message))

        element = super(_XiVOBrowserMixin, self).find_element(by, value)

        try:
            WebDriverWait(self, timeout).until(
                lambda browser: super(_XiVOBrowserMixin, self).find_element(by, value).is_displayed())
        except TimeoutException:
            raise ElementNotVisibleException('%s: %s' % (value, message))

        return element

    def find_element_by_id(self, id, message='', timeout=None):
        return self.find_element(By.ID, id, message, timeout)

    def find_element_by_name(self, name, message='', timeout=None):
        return self.find_element(By.NAME, name, message, timeout)

    def find_element_by_xpath(self, xpath, message='', timeout=None):
        return self.find_element(By.XPATH, xpath, message, timeout)

    def find_element_by_class_name(self, xpath, message='', timeout=None):
        return self.find_element(By.CLASS_NAME, xpath, message, timeout)

    def find_element_by_css_selector(self, xpath, message='', timeout=None):
        return self.find_element(By.CSS_SELECTOR, xpath, message, timeout)

    def find_element_by_label(self, label):
        """Finds the first element corresponding to the label containing the argument."""
        webelement_label = self.find_element_by_xpath(
            "//label[text() = '%s' or text() = '%s:']" % (label, label))
        webelement_id = webelement_label.get_attribute('for')
        webelement = self.find_element_by_id(webelement_id)
        return webelement

    def find_elements(self, by=By.ID, value=None, message='', timeout=None):
        """This function is called by all find_element_by_*().
           This implementation adds a timeout to search for Webelements."""
        # Do not call lambda browser : browser.find_element -> infinite recursion
        if timeout is None:
            timeout = world.timeout

        try:
            WebDriverWait(self, timeout).until(
                lambda browser: super(_XiVOBrowserMixin, self).find_elements(by, value))
        except TimeoutException:
            raise NoSuchElementException('%s: %s' % (value, message))

        return super(_XiVOBrowserMixin, self).find_elements(by, value)

    def find_elements_by_id(self, xpath, message='', timeout=None):
        return self.find_elements(By.ID, xpath, message, timeout)

    def find_elements_by_xpath(self, xpath, message='', timeout=None):
        return self.find_elements(By.XPATH, xpath, message, timeout)

    def find_elements_by_css_selector(self, xpath, message='', timeout=None):
        return self.find_elements(By.CSS_SELECTOR, xpath, message, timeout)

    def find_elements_by_tag_name(self, xpath, message='', timeout=None):
        return self.find_elements(By.TAG_NAME, xpath, message, timeout)

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
            alert = super(_XiVOBrowserMixin, self).switch_to_alert()
            time.sleep(1)
            if alert:
                return alert
            count += 1
        raise Exception(message)


class _XiVORemoteBrowserImplementation(_XiVOBrowserMixin, webdriver.Remote):

    def __init__(self, debug=False):
        self._debug = debug
        super(_XiVORemoteBrowserImplementation, self).__init__(command_executor='http://localhost:4444/wd/hub',
                                                               desired_capabilities=DesiredCapabilities.FIREFOX,
                                                               browser_profile=self._setup_browser_profile())


class _XiVOLocalBrowserImplementation(_XiVOBrowserMixin, webdriver.Firefox):

    def __init__(self, debug=False):
        self._debug = debug
        super(_XiVOLocalBrowserImplementation, self).__init__(firefox_profile=self._setup_browser_profile())
