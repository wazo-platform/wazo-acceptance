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

from hamcrest.core import assert_that
from hamcrest.library.collection.isdict_containingentries import has_entries
from hamcrest.library.collection.isdict_containingkey import has_key
from lettuce import step
from lettuce.registry import world

from xivo_acceptance.action.restapi import cti_profile_action_restapi
from xivo_acceptance.helpers import cti_profile_helper
from hamcrest.core.core.isnone import not_none


@step(u'Given I have the following CTI profiles:$')
def given_i_have_the_following_cti_profiles(step):
    for profile in step.hashes:
        cti_profile_helper.create_profile(profile)

@step(u'When I acces the list of CTI profiles$')
def when_i_acces_the_list_of_cti_profiles(step):
    world.response = cti_profile_action_restapi.all_profiles()

@step(u'Then I get a list containing the following CTI profiles:$')
def then_i_get_a_list_containing_the_following_cti_profiles(step):
    profile_response = world.response.data
    expected_profiles = _perform_casts(step.hashes)

    assert_that(profile_response, has_key('items'))
    profiles = profile_response['items']

    for expected_profile in expected_profiles:
        corresponding = _get_by_id(profiles, int(expected_profile['id']))
        assert_that(corresponding, not_none())
        assert_that(corresponding, has_entries(expected_profile))

@step(u'When I ask for the CTI profile with id "([^"]*)"$')
def when_i_ask_for_the_cti_profile_with_id_group1(step, profileid):
    world.response = cti_profile_action_restapi.get_cti_profile(profileid)

@step(u'Then I get a CTI profile with the following parameters:$')
def then_i_get_a_cti_profile_with_the_following_parameters(step):
    profile_response = world.response.data
    expected_profile = _perform_casts(step.hashes)[0]
    assert_that(profile_response, has_entries(expected_profile))

def _get_by_id(profiles, profileid):
    for profile in profiles:
        if profile['id'] == profileid:
            return profile
    return None

def _perform_casts(hashes):
    values = hashes
    for value in values:
        if 'id' in value:
            value['id'] = int(value['id'])
    return values
