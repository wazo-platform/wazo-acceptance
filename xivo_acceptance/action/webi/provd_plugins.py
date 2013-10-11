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

from lettuce.registry import world
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException

from xivo_acceptance.action.webi import provd_general as provd_general_action_webi
from xivo_lettuce import common


def update_plugin_list(url, check_confirmation=True):
    provd_general_action_webi.update_plugin_server_url(url)
    common.open_url('provd_plugin')
    world.browser.find_element_by_id('toolbar-bt-update').click()
    wait_time = 7
    if check_confirmation:
        _check_for_confirmation_message(wait_time)
    else:
        time.sleep(wait_time)


def _check_for_confirmation_message(secs):
    time.sleep(secs)
    try:
        world.browser.find_element_by_xpath("//div[@class[contains(.,'xivo-info')]]")
    except NoSuchElementException:
        errors = world.browser.find_element_by_xpath("//div[@class[contains(.,'xivo-error')]]").text
        raise Exception('Error during operation on plugins. Webi says:\n%s' % errors)


def plugins_successfully_updated():
    try:
        div = world.browser.find_element_by_id('report-xivo-info')
        return div is not None
    except (NoSuchElementException, ElementNotVisibleException):
        return False


def plugins_error_during_update():
    try:
        div = world.browser.find_element_by_id('report-xivo-error')
        return div is not None
    except (NoSuchElementException, ElementNotVisibleException):
        return False


def uninstall_plugin(plugin):
    common.open_url('provd_plugin')
    plugin_line = common.get_line(plugin)

    uninstall_btn = _find_uninstall_btn(plugin_line)

    if uninstall_btn:
        uninstall_btn.click()
        alert = world.browser.switch_to_alert()
        alert.accept()


def _find_uninstall_btn(plugin_line):
    try:
        return plugin_line.find_element_by_xpath(".//a[@title='Uninstall']")
    except (NoSuchElementException, ElementNotVisibleException):
        return None


def install_plugin(plugin):
    common.open_url('provd_plugin')
    plugin_line = common.get_line(plugin)

    install_btn = _find_install_btn(plugin_line)

    if install_btn:
        install_btn.click()
        _check_for_confirmation_message(2)


def _find_install_btn(plugin_line):
    try:
        return plugin_line.find_element_by_xpath(".//a[@title='Install']")
    except (NoSuchElementException, ElementNotVisibleException):
        return None


def install_firmware(firmware):
    firmware_line = _find_firmware_line(firmware)
    install_btn = firmware_line.find_element_by_xpath(".//a[@title='Install']")
    install_btn.click()

    _check_for_confirmation_message(10)


def _find_firmware_line(firmware):
    xpath = "//table[@id='tb-list-pkgs']//tr[contains(td[1], '%s')]" % firmware
    return world.browser.find_element_by_xpath(xpath)
