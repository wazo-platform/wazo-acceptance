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

from selenium.common.exceptions import NoSuchElementException
from xivo_lettuce import common, form
from xivo_lettuce.form.submit import submit_form_with_errors
import hamcrest


def create_campaign(info):
    common.open_url('campaign', 'add')
    fill_form(info)
    form.submit.submit_form()


def edit_campaign(name, info):
    common.edit_line(name)
    fill_form(info)
    form.submit.submit_form()


def add_or_replace(name):
    common.remove_element_if_exist('campaign', name)
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


def remove_recordings(campaign_name):
    common.open_url('campaign', 'list')
    line = common.get_line(campaign_name)
    link = line.find_element_by_xpath(".//a[@title='%s']" % campaign_name)
    link.click()
    common.remove_all_elements_from_current_page('')


def remove_campaign(name):
    common.open_url('campaign', 'list')
    common.remove_line(name)


def create_campaign_with_errors(infos):
    common.open_url('campaign', 'add')
    fill_form(infos)
    submit_form_with_errors()


def campaign_exists(info):
    common.open_url('campaign', 'list', None)
    line = common.get_line(info['name'])
    for value in info.values():
        try:
            line.find_element_by_xpath(".//td[contains(.,'%s')]" % value)
            hamcrest.assert_that(True)
        except NoSuchElementException:
            hamcrest.assert_that(False, "The campaign was not found in the list.")
