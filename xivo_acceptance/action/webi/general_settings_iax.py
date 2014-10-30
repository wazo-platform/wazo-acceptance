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

from lettuce.registry import world
from selenium.common.exceptions import NoSuchElementException
from xivo_acceptance.lettuce import common, form


def find_call_limit_line(destination=None, netmask=None, limit=None):
    common.open_url('general_iax')
    common.go_to_tab('Call limits')
    xpath = _xpath_call_limit_line(destination, netmask, limit)
    line = world.browser.find_element_by_xpath(xpath)
    return line


def find_call_limit_lines(destination=None, netmask=None, limit=None):
    common.open_url('general_iax')
    common.go_to_tab('Call limits')
    xpath = _xpath_call_limit_line(destination, netmask, limit)
    lines = world.browser.find_elements_by_xpath(xpath)
    return lines


def type_iax_call_limit(call_limit):
    address = call_limit['address']
    netmask = call_limit['netmask']
    call_count = call_limit['call_count']
    add_button = world.browser.find_element_by_xpath("//a[@title='Add a call limit']")
    add_button.click()
    world.new_line = world.browser.find_elements_by_xpath("//tbody[@id='disp']//tr")[-1]
    input_destination = world.new_line.find_element_by_name('calllimits[destination][]')
    input_destination.send_keys(address)
    input_netmask = world.new_line.find_element_by_name('calllimits[netmask][]')
    input_netmask.send_keys(netmask)
    input_limit = world.new_line.find_element_by_name('calllimits[calllimits][]')
    input_limit.send_keys(call_count)


def remove_call_limit_if_exists(destination, netmask):
    call_limits_to_remove = [{'address': destination, 'netmask': netmask}]
    try:
        remove_call_limits(call_limits_to_remove)
    except NoSuchElementException:
        pass


def remove_call_limits(call_limits):
    common.open_url('general_iax')
    common.go_to_tab('Call limits')
    for call_limit in call_limits:
        lines = find_call_limit_lines(call_limit['address'], call_limit['netmask'])
        for line in lines:
            delete_button = line.find_element_by_xpath(".//a[@title='Delete this limit']")
            delete_button.click()
        form.submit.submit_form()


def _xpath_call_limit_line(destination=None, netmask=None, limit=None):
    xpath = "//tbody[@id='disp']/tr"
    filters = []
    if destination is not None:
        filters.append("td/input[@name='calllimits[destination][]' "
                       "         and @value='%s']" % destination)
    if netmask is not None:
        filters.append("td/input[@name='calllimits[netmask][]' "
                       "         and @value='%s']" % netmask)
    if limit is not None:
        filters.append("td/input[@name='calllimits[calllimits][]' "
                       "         and @value='%s']" % limit)
    if len(filters) > 0:
        xpath += "[" + ' and '.join(filters) + "]"
    return xpath
