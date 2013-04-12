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

from selenium.common.exceptions import NoSuchElementException
from xivo_lettuce import form
from xivo_lettuce.common import open_url, find_line, edit_line, remove_line

def create_campaign(info):
    open_url('campaign', 'add')
    fill_form(info)

def edit_campaign(name, info):
    edit_line(name)
    fill_form(info)

def add_or_replace(name):
    try:
        find_line(name)
    except NoSuchElementException:
        create_campaign({'name': name})

def fill_form(info):
    if 'name' in info:
        form.input.edit_text_field_with_id('recordingcampaign_name', info['name'])
    if 'start_date' in info:
        form.input.edit_text_field_with_id('it-start_date', info['start_date'])
    if 'end_date' in info:
        form.input.edit_text_field_with_id('it-end_date', info['end_date'])
    if 'queue' in info:
        form.select.set_select_field_with_id_containing("recordingcampaign_queueid", info['queue'])
    form.submit.submit_form()

def remove_recordings(campaign_name):
    open_url('campaign', 'list')
    line = find_line(campaign_name)
    link = line.find_element_by_xpath(".//a[@title='%s']" % campaign_name)
    link.click()
    got_exception = False
    while not got_exception:
        try:
            remove_line('')
        except NoSuchElementException:
            got_exception = True

def remove_campaign(name):
    open_url('campaign', 'list')
    remove_line(name)
