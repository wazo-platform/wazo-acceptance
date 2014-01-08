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

from lettuce import step

from xivo_acceptance.action.webi import campaign as campaign_action_webi
from xivo_lettuce import common


@step(u'Given there is no campaign "([^"]*)"$')
def given_there_is_no_element(step, search):
    common.remove_element_if_exist('campaign', search)


@step(u'When I create a campaign with the following parameters:')
def when_i_create_a_campaign_with_the_following_parameters(step):
    params = step.hashes[0]
    campaign_action_webi.create_campaign(params)


@step(u'Then there is a campaign in the list with the following values:')
def then_there_is_a_campaign_in_the_list_with_the_following_values(step):
    for info in step.hashes:
        campaign_action_webi.campaign_exists(info)


@step(u'Given there is a campaign "([^"]*)"$')
def given_there_is_a_campaign(step, name):
    campaign_action_webi.add_or_replace(name)


@step(u'When I edit the campaign "([^"]*)" with the values:')
def when_i_edit_the_campaign_with_the_values(step, name):
    campaign_action_webi.edit_campaign(name, step.hashes[0])


@step(u'Given there is a campaign "([^"]*)" with no recording$')
def given_there_is_a_campaign_with_no_recording(step, name):
    step.given('Given there is a campaign "%s"' % name)
    campaign_action_webi.remove_recordings(name)


@step(u'When I delete the campaign "([^"]*)"')
def when_i_delete_the_campaign(step, name):
    campaign_action_webi.remove_campaign(name)


@step(u'When I try to create a campaign with the following parameters:')
def when_i_try_to_create_a_campaign_with_the_following_parameters(step):
    for info in step.hashes:
        campaign_action_webi.create_campaign_with_errors(info)
