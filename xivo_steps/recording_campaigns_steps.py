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

from lettuce import step
from selenium.common.exceptions import NoSuchElementException
from xivo_lettuce.common import open_url, find_line, remove_line
from xivo_lettuce.manager import campaign_manager

@step(u'When I create a campaign with the following parameters:')
def when_i_create_a_campaign_with_the_following_parameters(step):
    params = step.hashes[0]
    campaign_manager.create_campaign(params)

@step(u'Then there is a campaign in the list with the following values:')
def then_there_is_a_campaign_in_the_list_with_the_following_values(step):
    params = step.hashes[0]
    open_url('campaign', 'list', None)
    name = params['name']
    line = find_line(name)
    for value in params.values():
        try:
            line.find_element_by_xpath(".//td[contains(.,'%s')]" % value)
            assert True
        except NoSuchElementException:
            assert False

@step(u'Given there is a campaign "([^"]*)"$')
def given_there_is_a_campaign(step, name):
    campaign_manager.add_or_replace(name)

@step(u'When I edit the campaign "([^"]*)" with the values:')
def when_i_edit_the_campaign_with_the_values(step, name):
    campaign_manager.edit_campaign(name, step.hashes[0])

@step(u'Given there is a campaign "([^"]*)" with no recording$')
def given_there_is_a_campaign_with_no_recording(step, name):
    step.given('Given there is a campaign "%s"' % name)
    campaign_manager.remove_recordings(name)

@step(u'When I delete the campaign "([^"]*)"')
def when_i_delete_the_campaign(step, name):
    campaign_manager.remove_campaign(name)

@step(u'When I try to create a campaign with the following parameters:')
def when_i_try_to_create_a_campaign_with_the_following_parameters(step):
    params = step.hashes[0]
    campaign_manager.create_campaign_with_errors(params)
