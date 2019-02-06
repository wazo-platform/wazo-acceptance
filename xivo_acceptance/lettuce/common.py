# -*- coding: utf-8 -*-
# Copyright 2013-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals

import time
import urllib

from lettuce.registry import world
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import (
    staleness_of,
    visibility_of,
)

from form.checkbox import Checkbox
from xivo_acceptance.action.webi import common as common_action_webi
from xivo_acceptance.lettuce import urls


def webi_login(login, password, language):
    query = {
        'login': login,
        'password': password,
        'language': language,
        'go': '/service/ipbx/index.php'
    }
    open_url('login', None, query)


def webi_login_as_default():
    webi_login(world.config['frontend']['username'],
               world.config['frontend']['passwd'],
               'en')


def waitForLoginPage():
    world.browser.find_element_by_id('it-login', 'login page not loaded', 30)


def webi_logout():
    open_url('logout')


def the_option_is_checked(option_label, checkstate=True, **kwargs):
    """Read or change the value of a checkbox.

    When reading the value of a checkbox, an AssertionError will be raised
    if the checkbox value is different from `checkstate`.

    Arguments:

        - option_label -- the checkbox's label (visible text). Used for finding
          the checkbox.

        - checkstate -- True or False, used to set the checkbox's value.

    Keyword arguments:

        - given -- If True, then read the checkbox's value.  Otherwise, set the
          checkbox's value to `checkstate`

    For example, given the following html snippit::

        <form>
            <label for="checkme_id">Check me !</label>
            <input id="checkme_id" type="checkbox">the checkbox</input>
        </form>

    The function can be used as follows::

        >>> #make sure the checkbox is checked
        >>> from xivo_acceptance.lettuce import common
        >>> common.the_option_is_checked('Check me !', True, given=True)
        >>>
        >>> #uncheck the checkbox
        >>> common.the_option_is_checked('Check me !', False)
    """
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

    return bool(find_line(search))


def element_is_not_in_list(module, search, qry=None, action='list'):
    return not element_is_in_list(module, search, qry=qry, action=action)


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

    url = build_url(uri, qry)

    world.browser.get(url)


def build_url(uri, query={}):
    if not uri.startswith('/'):
        uri = '/%s' % uri

    url = '%s%s' % (world.config['frontend']['url'], uri)

    qry_encode = urllib.urlencode(query)
    if qry_encode:
        url = '%s?%s' % (url, qry_encode)

    return url


def get_line(search, column=None):
    """Return the tr webelement of a line in a list.

    Used for executing operations, like clicking on a button or extracting
    information, on an element in a list. Returns a Selenium WebElement.

    Arguments:

        - search -- Search for a line that contains the text `search`
        - column -- Optional: The label of the column containing the text `search`.
          The matching becomes exact.

    Given the following html::

        <table id="table-main-listing">
            <tr>
                <td>User: John Doe</td>
                <td>Number: 555-123-4567</td>
                <td><a href="#">Edit</a></td>
            <tr>
            <tr>
                <td>User: Roger Smith</td>
                <td>Number: 555-765-4321</td>
                <td><a href="#">Edit</a></td>
            <tr>
        </table>

    The function can be used as follows::

        >>> #fetch the line that as the phone number '555-123-4567'
        >>> from xivo_acceptance.lettuce import common
        >>> line = common.get_line('555-1234-4567')
        >>>
        >>> #do stuff with `line`
    """
    if column:
        xpath = ('//table[@id="table-main-listing"]' +
                 '//tr[@class="sb-top"]' +
                 '/th[text()="{column}"]/preceding-sibling::th').format(column=column)
        column_position = len(world.browser.find_elements_by_xpath(xpath)) + 1
        td_filter = 'td[position()={position} and @title="{text}"]'.format(position=column_position, text=search)
        xpath = ('//table[@id="table-main-listing"]' +
                 '//tr[contains(@class,"sb-content") and {td_filter}]').format(td_filter=td_filter)
        tr_element_containing_the_cell = world.browser.find_element_by_xpath(xpath)
        return tr_element_containing_the_cell
    else:
        xpath = "//table[@id='table-main-listing']//tr[contains(.,'{text}')]".format(text=search)
        return world.browser.find_element_by_xpath(xpath)


def get_lines(line_substring):
    return world.browser.find_elements_by_xpath(
        "//table[@id='table-main-listing']//tr[contains(.,'%s')]" % line_substring)


def find_line(line_substring, column=None):
    try:
        return get_line(line_substring, column)
    except NoSuchElementException:
        return None


def find_lines(line_substring):
    try:
        return get_lines(line_substring)
    except NoSuchElementException:
        return []


def find_line_and_fetch_col(line_substring, class_name):
    """Find a line in a list and return one of its columns .

    Used for executing operations, like clicking on a button or extracting
    information, on an element in a list. Returns a Selenium WebElement.

    Arguments:

        - line_substring -- Search for a line that contains `line_substring` in
          the column

        - class_name -- CSS class name of the column.

    Given the following html::

        <table id="table-main-listing">
            <tr>
                <td class="txt-left">John Doe</td>
                <td class="txt-center">555-123-4567</td>
                <td class="txt-right"><a href="#">Edit</a></td>
            <tr>
            <tr>
                <td class="txt-left">Roger Smith</td>
                <td class="txt-center">555-987-6543</td>
                <td class="txt-right"><a href="#">Edit</a></td>
            <tr>
        </table>

    The function can be used as follows::

        >>> from xivo_acceptance.lettuce import common
        >>> column = common.find_line_and_fetch_col("Roger Smith", "txt-left")
        >>> name = column.get_attribute('value')
    """
    return world.browser.find_element_by_xpath(
        ".//*[@id='table-main-listing']/tbody/tr[contains(.,'%s')]/td[@class='%s']" % (line_substring, class_name))


def remove_element_if_exist(module, search, column=None):
    open_url(module, 'list')
    try:
        remove_line(search, column)
    except (NoSuchElementException, ElementNotVisibleException):
        pass


def remove_all_elements(module, search, column=None):
    open_url(module, 'list')
    remove_all_elements_from_current_page(search, column)


def remove_all_elements_from_current_page(search, column=None):
    try:
        while True:
            remove_line(search, column)
    except (NoSuchElementException, ElementNotVisibleException):
        pass


def remove_line(line_substring, column=None):
    """Remove a line in a list by clicking on the delete button.

    Arguments:

        - line_substring -- Search for the line that contains the text
          `line_substring`
    """
    click_on_line_with_alert('Delete', line_substring, column)


def click_checkbox_for_all_lines():
    for checkbox in world.browser.find_elements_by_css_selector(".it-checkbox"):
        checkbox.click()


def click_on_line_with_alert(act, line_substring, column=None):
    table_line = get_line(line_substring, column)
    common_action_webi.reset_focus()
    delete_button = table_line.find_element_by_xpath(".//a[@title='%s']" % act)
    delete_button.click()
    alert = world.browser.switch_to_alert()
    alert.accept()
    WebDriverWait(world.browser, 15).until(staleness_of(delete_button))


def disable_selected_lines():
    common_action_webi.reset_focus()

    menu_button = world.browser.find_element_by_id("toolbar-bt-advanced")
    WebDriverWait(world.browser, world.timeout).until(visibility_of(menu_button))
    ActionChains(world.browser).move_to_element(menu_button).perform()

    disable_button = world.browser.find_element_by_id("toolbar-advanced-menu-disable")
    WebDriverWait(world.browser, world.timeout).until(visibility_of(disable_button))
    disable_button.click()


def edit_line(line_substring, column=None):
    """Edit an element in a list by clicking on the edit button

    Arguments:

        - line_substring -- Search for the line that contains the text
          `line_substring`
    """
    table_line = get_line(line_substring, column)
    edit_button = table_line.find_element_by_xpath(".//a[@title='Edit']")
    edit_button.click()


def enable_selected_lines():
    menu_button = world.browser.find_element_by_id("toolbar-bt-advanced")
    ActionChains(world.browser).move_to_element(menu_button).perform()

    enable_button = world.browser.find_element_by_id("toolbar-advanced-menu-enable")
    WebDriverWait(world.browser, world.timeout).until(visibility_of(enable_button))
    enable_button.click()


def go_to_tab(tab_label, ss_tab_label=None):
    """Click a tab button inside a form.

    Used when switching to another tab inside a form.

    Arguments:

        - tab_label -- Label of the tab to switch to.
    """
    common_action_webi.reset_focus()
    tab_button = world.browser.find_element_by_xpath("//div[@class='tab']//a[contains(.,'%s')]" % tab_label)
    if ss_tab_label:
        ss_tab = tab_button.find_element_by_xpath("//div[@class='stab']//a[contains(.,'%s')]" % ss_tab_label)
        WebDriverWait(world.browser, world.timeout).until(visibility_of(tab_button))
        ActionChains(world.browser).move_to_element(tab_button).perform()
        WebDriverWait(world.browser, world.timeout).until(visibility_of(ss_tab))
        ss_tab.click()
    else:
        tab_button.click()
    time.sleep(1)


def get_host_address():
    host = world.config['frontend']['url']
    host = host.rstrip('/')
    host = host.partition('//')[2]
    return host


class NoMoreTries(Exception):
    pass


def wait_until(function, *args, **kwargs):
    """Run <function> <tries> times, spaced with 1 second. Stops when <function>
    returns an object evaluating to True, and returns it.

    Useful for waiting for an event.

    Arguments:

        - function: the function detecting the event
        - message: the message raised if <function> does not return something
          after <tries> times
        - tries: the number of times to run <function>
    """

    message = kwargs.pop('message', None)
    tries = kwargs.pop('tries', 1)
    return_value = False

    for _ in xrange(tries):
        return_value = function(*args, **kwargs)
        if return_value:
            return return_value
        time.sleep(1)
    else:
        raise NoMoreTries(message)


def wait_until_assert(assert_function, *args, **kwargs):
    """Run <assert_function> <tries> times, spaced with 1 second. Stops when
    <function> does not throw AssertionError.

    Useful for waiting until an assert is True (or assert_that from hamcrest).

    Arguments:

        - assert_function: the function making the assertion
        - tries: the number of times to run <function>
    """
    tries = kwargs.pop('tries', 1)
    errors = []

    for _ in xrange(tries):
        try:
            assert_function(*args, **kwargs)
            return
        except AssertionError as e:
            errors.append(str(e))
            time.sleep(1)
    else:
        raise NoMoreTries('\n'.join(errors))


def assert_over_time(assert_function, *args, **kwargs):
    """Run <assert_function> <tries> times, spaced with 1 second. Stops if
    <function> throws AssertionError.

    Useful for checking that an assert (or hamcrest.assert_that) is still
    True after some time, e.g. an event that should not happen.

    Arguments:

        - assert_function: the function making the assertion
        - tries: the number of times to run <function>
    """
    tries = kwargs.pop('tries', 2)

    for _ in xrange(tries):
        assert_function(*args, **kwargs)
        time.sleep(1)
