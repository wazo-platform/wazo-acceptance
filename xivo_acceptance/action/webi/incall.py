# -*- coding: utf-8 -*-

# Copyright (C) 2013-2016 Avencall
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
from selenium.webdriver.support.select import Select
from xivo_acceptance.lettuce import common

DESTINATION_ELEMENT_MAP = {
    'Queue': 'it-dialaction-answer-queue-actionarg1',
    'User': 'it-dialaction-answer-user-actionarg1',
    'Group': 'it-dialaction-answer-group-actionarg1',
}


def type_incall_did(incall_did):
    world.browser.find_element_by_id('it-incall-exten', 'Incall form not loaded')
    world.incall_did = incall_did
    input_did = world.browser.find_element_by_id('it-incall-exten')
    input_did.send_keys(incall_did)


def type_incall_context(incall_context):
    input_context = Select(world.browser.find_element_by_id('it-incall-context'))
    input_context.select_by_value(incall_context)


def type_incall_destination(destination_type, destination_name):
    type_select = Select(world.browser.find_element_by_id('it-dialaction-answer-actiontype'))
    type_select.select_by_visible_text(destination_type)
    destination_select = Select(world.browser.find_element_by_id(DESTINATION_ELEMENT_MAP[destination_type]))
    for option in destination_select.options:
        if destination_name in option.text:
            destination_select.select_by_visible_text(option.text)


def type_incall_schedule(schedule):
    common.go_to_tab('Schedules')
    schedule_select = Select(world.browser.find_element_by_id('it-schedule_id'))
    schedule_select.select_by_visible_text(schedule)


def remove_incall_with_did(incall_did):
    common.remove_element_if_exist('incall', incall_did)


def search_incall_number(did):
    common.open_url('incall')
    searchbox_id = 'it-toolbar-search'
    text_input = world.browser.find_element_by_id(searchbox_id)
    text_input.clear()
    text_input.send_keys(did)
    submit_button = world.browser.find_element_by_id('it-subsearch')
    submit_button.click()
