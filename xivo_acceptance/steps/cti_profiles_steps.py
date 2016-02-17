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

from hamcrest.core import assert_that
from hamcrest.library.collection.isdict_containingentries import has_entries
from hamcrest.library.collection.isdict_containingkey import has_key
from lettuce import step
from lettuce.registry import world

from xivo_acceptance.action.confd import cti_profile_action_confd
from xivo_acceptance.helpers import cti_profile_helper, user_helper
from hamcrest.core.core.isnone import not_none, none


@step(u'Given I have the following CTI profiles:$')
def given_i_have_the_following_cti_profiles(step):
    for profile in step.hashes:
        cti_profile_helper.add_or_replace_profile(profile)


@step(u'Given the following users, CTI profiles are linked:$')
def given_the_following_users_cti_profiles_are_linked(step):
    for user_profile in step.hashes:
        _create_association(user_profile)


@step(u'When I access the list of CTI profiles$')
def when_i_acces_the_list_of_cti_profiles(step):
    world.response = cti_profile_action_confd.all_profiles()


@step(u'When I ask for the CTI profile with id "([^"]*)"$')
def when_i_ask_for_the_cti_profile_with_id_group1(step, profileid):
    world.response = cti_profile_action_confd.get_cti_profile(profileid)


@step(u'When I associate CTI profile "([^"]*)" with user "([^"]*)" "([^"]*)"$')
def when_i_associate_cti_profile_group1_with_user_group2_group3(step, cti_profile_id, firstname, lastname):
    user_id = user_helper.get_user_id_with_firstname_lastname(firstname, lastname)
    world.response = cti_profile_action_confd.associate_profile_to_user(int(cti_profile_id), int(user_id))


@step(u'When I activate the CTI client for user "([^"]*)" "([^"]*)"$')
def when_i_activate_the_cti_client_for_user_group1_group2(step, firstname, lastname):
    user_helper.enable_cti_client(firstname, lastname)


@step(u'When I associate CTI profile with name "([^"]*)" with user "([^"]*)" "([^"]*)"')
def when_i_associate_cti_profile_with_name_group1_with_user_group2_group3(step, cti_profile_name, firstname, lastname):
    cti_profile_id = cti_profile_helper.get_id_with_name(cti_profile_name)
    user_id = user_helper.get_user_id_with_firstname_lastname(firstname, lastname)
    world.response = cti_profile_action_confd.associate_profile_to_user(cti_profile_id, int(user_id))


@step(u'When I send request for the CTI configuration of the user "([^"]*)" "([^"]*)"$')
def when_i_send_request_for_the_cti_configuration_of_the_user_group1_group2(step, firstname, lastname):
    user_id = user_helper.get_user_id_with_firstname_lastname(firstname, lastname)
    world.response = cti_profile_action_confd.get_cti_profile_for_user(user_id)


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


@step(u'Then I get a response with a null CTI profile')
def then_i_get_a_response_with_a_null_cti_profile(step):
    profile_response = world.response.data
    assert_that(profile_response['cti_profile_id'], none())


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


def _create_association(association_infos):
    firstname, lastname = association_infos['firstname'], association_infos['lastname']
    userid = user_helper.get_user_id_with_firstname_lastname(firstname, lastname)
    profileid = association_infos['cti_profile_id']
    cti_profile_action_confd.associate_profile_to_user(int(profileid), int(userid))
