# -*- coding: utf-8 -*-
# Copyright (C) 2013-2014 Avencall
# SPDX-License-Identifier: GPL-3.0+

import time

from lettuce import world
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.select import Select

from xivo_acceptance.helpers import user_line_extension_helper as ule_helper
from xivo_acceptance.lettuce import common
from xivo_acceptance.lettuce.exception import NoSuchProfileException
from xivo_acceptance.lettuce.form.list_pane import ListPane


def delete_profile(profile_label):
    ule_helper.delete_users_with_profile(profile_label)
    common.open_url('profile', 'list')
    common.remove_line(profile_label)


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


def add_xlet(xlet_label, xlet_position='dock'):
    """Add a xlet."""
    add_button = world.browser.find_element_by_xpath(
        "//table[@id = 'list_xlet']//a[@id = 'lnk-add-row']")
    add_button.click()
    time.sleep(1)

    input_line = world.browser.find_elements_by_xpath(
        "//table[@id = 'list_xlet']//tr")[-2]
    input_xlet_name = Select(input_line.find_element_by_xpath(
        ".//select[@name = 'xlet[id][]']"))
    input_xlet_name.select_by_visible_text(xlet_label)

    input_xlet_position = Select(input_line.find_element_by_xpath(
        ".//select[@name = 'xlet[layout][]']"))
    input_xlet_position.select_by_visible_text(xlet_position)


def _get_services_list():
    return ListPane.from_id('servicelist')
