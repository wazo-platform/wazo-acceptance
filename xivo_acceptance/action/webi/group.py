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

from lettuce import world
from xivo_lettuce import common


def type_group_name(group_name):
    world.browser.find_element_by_id('it-groupfeatures-name', 'Group form not loaded')
    world.group_name = group_name
    input_name = world.browser.find_element_by_id('it-groupfeatures-name')
    input_name.send_keys(group_name)


def type_group_number(group_number):
    world.browser.find_element_by_id('it-groupfeatures-number', 'Group form not loaded')
    world.group_number = group_number
    input_number = world.browser.find_element_by_id('it-groupfeatures-number')
    input_number.send_keys(group_number)


def type_context(context):
    select_context = world.browser.find_element_by_xpath(
        '//select[@id="it-groupfeatures-context"]//option[@value="%s"]' % context)
    select_context.click()


def remove_group_with_name(group_name):
    common.remove_element_if_exist('group', group_name)
