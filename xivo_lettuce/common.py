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

import urllib
import time

from lettuce.registry import world
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException
from form.checkbox import Checkbox
from xivo_lettuce import urls
from xivo_lettuce.form import submit
from selenium.webdriver.common.action_chains import ActionChains


def get_value_with_label(field_label):
    element = world.browser.find_element_by_label(field_label)
    return element.get_attribute('value')


def webi_login(user, password, language):
    input_login = world.browser.find_element_by_id('it-login')
    input_password = world.browser.find_element_by_id('it-password')
    input_login.send_keys(user)
    input_password.send_keys(password)
    language_option = world.browser.find_element_by_xpath('//option[@value="%s"]' % language)
    language_option.click()
    submit.submit_form()
    world.browser.find_element_by_id('loginbox', 'Cannot login as ' + user)
    world.logged = True


def webi_login_as_default():
    webi_login(world.login, world.password, 'en')


def waitForLoginPage():
    world.browser.find_element_by_id('it-login', 'login page not loaded', 30)


def webi_logout():
    logout = '/xivo/logoff.php'
    url = '%s%s' % (world.host, logout)
    world.browser.get(url)


def the_option_is_checked(option_label, checkstate, **kwargs):
    """Reads or write the value of a checkbox, selected by its label text.
       Use given = True if you want to set the checkbox"""
    # If given, then we set the option.
    # If not given, we assert the option is in checkstate.
    if 'given' in kwargs:
        given = kwargs['given']
    else:
        given = False

    # Get the webelement.
    world.last_option_label = option_label
    option = world.browser.find_element_by_label(option_label)

    # Determine the action to do.
    goal_checked = (checkstate is None)
    if not given:
        assert Checkbox(option).is_checked() == goal_checked
    else:
        Checkbox(option).set_checked(goal_checked)


def element_is_in_list(module, search, qry=None, action='list'):
    if qry is None:
        qry = {}
    open_url(module, action, qry)
    try:
        find_line(search)
    except NoSuchElementException:
        return False
    return True


def element_is_not_in_list(module, search, qry=None, action='list'):
    if qry is None:
        qry = {}
    open_url(module, action, qry)
    try:
        find_line(search)
    except NoSuchElementException:
        return True
    return False


def element_in_list_matches_field(module, search, class_name, value, qry=None, action='list'):
    if qry is None:
        qry = {}
    open_url(module, action, qry)
    try:
        line = find_line_and_fetch_col(search, class_name)
        assert int(line.text) == value
    except NoSuchElementException:
        return None


def open_url(module, act=None, qry=None):
    if qry is None:
        qry = {}
    list_url = urls.URLS
    if act:
        qry.update({'act': act})
    if module in list_url:
        uri = list_url[module]
    elif module in urls.ALIAS:
        module_alias = urls.ALIAS[module]['module']
        if 'qry' in urls.ALIAS[module]:
            qry.update(urls.ALIAS[module]['qry'])
        uri = list_url[module_alias]
    else:
        raise Exception("Unknown module : %s" % module)

    qry_encode = urllib.urlencode(qry)
    url = '%s%s' % (world.host, uri)
    if qry_encode:
        url = '%s?%s' % (url, qry_encode)
    world.browser.get(url)


def find_line(line_substring):
    """Return the tr webelement of a list table."""
    return world.browser.find_element_by_xpath(
        "//table[@id='table-main-listing']//tr[contains(.,'%s')]" % line_substring)


def find_line_and_fetch_col(line_substring, class_name):
    """Return the tr webelement of a list table."""
    return world.browser.find_element_by_xpath(
       ".//*[@id='table-main-listing']/tbody/tr[contains(.,'%s')]/td[@class='%s']" % (line_substring, class_name))


def remove_element_if_exist(module, search):
    open_url(module, 'list')
    try:
        remove_line(search)
    except (NoSuchElementException, ElementNotVisibleException):
        pass


def remove_all_elements(module, search):
    open_url(module, 'list')
    remove_all_elements_from_current_page(search)

def remove_all_elements_from_current_page(search):
    try:
        while True:
            remove_line(search)
    except (NoSuchElementException, ElementNotVisibleException):
        pass


def remove_line(line_substring):
    """Remove a line in a list table."""
    table_line = find_line(line_substring)
    delete_button = table_line.find_element_by_xpath(".//a[@title='Delete']")
    delete_button.click()
    alert = world.browser.switch_to_alert()
    alert.accept()


def edit_line(line_substring):
    """Edit an element of a list table."""
    table_line = find_line(line_substring)
    edit_button = table_line.find_element_by_xpath(".//a[@title='Edit']")
    edit_button.click()


def go_to_tab(tab_label, ss_tab_label=None):
    """Click a tab button."""
    tab_button = world.browser.find_element_by_xpath("//div[@class='tab']//a[contains(.,'%s')]" % tab_label)
    if ss_tab_label:
        hover = ActionChains(world.browser).move_to_element(tab_button)
        ss_tab_label = tab_button.find_element_by_xpath("//div[@class='stab']//a[contains(.,'%s')]" % ss_tab_label)
        hover.move_to_element(ss_tab_label)
        hover.click()
        hover.perform()
    else:
        tab_button.click()
    time.sleep(1)


def go_to_last_page():
    try:
        page_links = world.browser.find_elements_by_xpath("//div[@class='b-page']/a[starts-with(@title, 'Page ')]")
    except NoSuchElementException:
        pass
    else:
        last_page_link = page_links[-1]
        last_page_link.click()


def get_host_address():
    host = world.host
    host = host.rstrip('/')
    host = host.partition('//')[2]
    return host


def go_to_home_page():
    home_page = '%s%s' % (world.host, '?go=%252Fservice%252Fipbx%252Findex.php')
    world.browser.get(home_page)


def logged():
    if world.logged:
        return True
    else:
        try:
            world.browser.find_element_by_id('loginbox')
            return True
        except NoSuchElementException:
            return False
