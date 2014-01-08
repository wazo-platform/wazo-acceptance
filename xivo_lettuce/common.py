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

import urllib
import time

from lettuce.registry import world
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException
from form.checkbox import Checkbox
from xivo_lettuce import urls
from selenium.webdriver.common.action_chains import ActionChains


def get_value_with_label(field_label):
    element = world.browser.find_element_by_label(field_label)
    return element.get_attribute('value')


def webi_login(login, password, language):
    query = {
        'login': login,
        'password': password,
        'language': language,
        'go': '/service/ipbx/index.php'
    }
    open_url('login', None, query)


def webi_login_as_default():
    webi_login(world.config.webi_login, world.config.webi_password, 'en')


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
        >>> from xivo_lettuce import common
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

    url = '%s%s' % (world.config.webi_url, uri)

    qry_encode = urllib.urlencode(query)
    if qry_encode:
        url = '%s?%s' % (url, qry_encode)

    return url


def get_line(line_substring):
    """Return the tr webelement of a line in a list.

    Used for executing operations, like clicking on a button or extracting
    information, on an element in a list. Returns a Selenium WebElement.

    Arguments:

        - line_substring -- Search for a line that contains the text
          `line_substring`

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
        >>> from xivo_lettuce import common
        >>> line = common.get_line('555-1234-4567')
        >>>
        >>> #do stuff with `line`
    """
    return world.browser.find_element_by_xpath(
        "//table[@id='table-main-listing']//tr[contains(.,'%s')]" % line_substring)


def find_line(line_substring):
    try:
        return get_line(line_substring)
    except NoSuchElementException:
        return None


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

        >>> from xivo_lettuce import common
        >>> column = common.find_line_and_fetch_col("Roger Smith", "txt-left")
        >>> name = column.get_attribute('value')
    """
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
    """Remove a line in a list by clicking on the delete button.

    Arguments:

        - line_substring -- Search for the line that contains the text
          `line_substring`
    """
    click_on_line_with_alert('Delete', line_substring)


def click_on_line_with_alert(act, line_substring):
    table_line = get_line(line_substring)
    delete_button = table_line.find_element_by_xpath(".//a[@title='%s']" % act)
    delete_button.click()
    alert = world.browser.switch_to_alert()
    alert.accept()


def edit_line(line_substring):
    """Edit an element in a list by clicking on the edit button

    Arguments:

        - line_substring -- Search for the line that contains the text
          `line_substring`
    """
    table_line = get_line(line_substring)
    edit_button = table_line.find_element_by_xpath(".//a[@title='Edit']")
    edit_button.click()


def go_to_tab(tab_label, ss_tab_label=None):
    """Click a tab button inside a form.

    Used when switching to another tab inside a form.

    Arguments:

        - tab_label -- Label of the tab to switch to.
    """
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


def get_host_address():
    host = world.config.webi_url
    host = host.rstrip('/')
    host = host.partition('//')[2]
    return host
