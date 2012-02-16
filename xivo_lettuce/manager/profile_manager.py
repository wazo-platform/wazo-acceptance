# -*- coding: utf-8 -*-

import time

from lettuce.registry import world
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.select import Select
from xivo_lettuce.common import *


def delete_profile(profile_label):
    open_url('ctiprofile', 'list')
    remove_line(profile_label)


def type_profile_names(id, display_name):
    input_id = world.browser.find_element_by_id('it-profiles-name')
    input_id.clear()
    input_id.send_keys(id)

    input_display_name = world.browser.find_element_by_id('it-profiles-appliname')
    input_display_name.clear()
    input_display_name.send_keys(display_name)


def add_service(service_label):
    """Add a service. If the service is already added, does nothing."""
    input_services_disabled = Select(world.browser.find_element_by_xpath(
        "//select[@id = 'it-serviceslist']"))
    try:
        input_services_disabled.select_by_visible_text(service_label)
    except NoSuchElementException:
        return
    input_add_button = world.browser.find_element_by_id('bt-inaccess_profiles')
    input_add_button.click()

    # Wait for the Javascript to add the service
    time.sleep(world.timeout)


def remove_service(service_label):
    """Remove a service. If the service is already removed, does nothing."""
    input_services_enabled = Select(world.browser.find_element_by_xpath(
        "//select[@id = 'it-services']"))
    try:
        input_services_enabled.select_by_visible_text(service_label)
    except NoSuchElementException:
        return
    input_remove_button = world.browser.find_element_by_id('bt-outaccess_profiles')
    input_remove_button.click()

    # Wait for the Javascript to add the service
    time.sleep(world.timeout)


def remove_all_services():
    """Removes all services."""
    options = input_services_enabled = world.browser.find_elements_by_xpath(
        "//select[@id = 'it-services']/option")
    for option in options:
        option.click()

    input_remove_button = world.browser.find_element_by_id('bt-outaccess_profiles')
    input_remove_button.click()

    # Wait for the Javascript to add the service
    time.sleep(world.timeout)


def add_xlet(xlet_label):
    """Add a xlet."""
    add_button = world.browser.find_element_by_xpath(
        "//table[tbody[@id = 'xlets']]//th[@class = 'th-right']/a")
    add_button.click()
    time.sleep(world.timeout)
    input_line = world.browser.find_elements_by_xpath(
        "//tbody[@id='xlets']//tr")[-1]
    input_xlet_name = Select(input_line.find_element_by_xpath(
        ".//select[@name = 'xletslist[]']"))
    input_xlet_name.select_by_visible_text(xlet_label)
