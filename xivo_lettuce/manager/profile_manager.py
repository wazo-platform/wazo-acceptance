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

import time
from lettuce import world
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.select import Select
from xivo_lettuce.common import open_url, remove_line
from xivo_lettuce.exception import NoSuchProfileException
from xivo_lettuce.form.list_pane import ListPane
from xivo_lettuce.manager_ws.user_manager_ws import delete_users_with_profile


def delete_profile(profile_label):
    delete_users_with_profile(profile_label)
    open_url('profile', 'list')
    remove_line(profile_label)


def delete_profile_if_exists(profile_label):
    try:
        delete_profile(profile_label)
    except (NoSuchProfileException, NoSuchElementException):
        pass


def type_profile_names(profile_name):
    input_id = world.browser.find_element_by_id('it-profiles-name')
    input_id.clear()
    input_id.send_keys(profile_name)


def selected_services():
    services_pane = _get_services_list()
    return services_pane.selected_labels()


def remove_all_services():
    services_pane = _get_services_list()
    services_pane.remove_all()


def add_xlet(xlet_label):
    """Add a xlet."""
    add_button = world.browser.find_element_by_xpath(
        "//table[tbody[@id = 'xlets']]//th[@class = 'th-right']/a")
    add_button.click()
    time.sleep(1)
    input_line = world.browser.find_elements_by_xpath(
        "//tbody[@id='xlets']//tr")[-1]
    input_xlet_name = Select(input_line.find_element_by_xpath(
        ".//select[@name = 'xlet[id][]']"))
    input_xlet_name.select_by_visible_text(xlet_label)


def _get_services_list():
    return ListPane.from_id('servicelist')
