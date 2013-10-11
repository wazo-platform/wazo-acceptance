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

from hamcrest import *
from lettuce import step, world

from xivo_acceptance.helpers import voicemail_helper
from xivo_acceptance.action.restapi import voicemail_action_restapi as voicemail_ws
from xivo_lettuce.xivo_hamcrest import assert_has_dicts_in_order, assert_does_not_have_any_dicts


@step(u'Given there is no voicemail with number "([^"]*)" and context "([^"]*)"')
def given_there_is_no_voicemail_with_number_and_context(step, voicemail_number, context):
    voicemail_helper.delete_voicemail_with_number_context(voicemail_number, context)


@step(u'Given I have no voicemail with id "([^"]*)"')
def given_i_have_no_voicemail_with_id_group1(step, voicemail_id):
    voicemail_helper.delete_voicemail_with_id(voicemail_id)


@step(u'Given I have the following voicemails:')
def given_have_the_following_voicemails(step):
    for row in step.hashes:
        voicemail_info = _extract_voicemail_info(row)
        voicemail_helper.add_or_replace_voicemail(voicemail_info)


def _extract_voicemail_info(row):
    voicemail = dict(row)

    if 'max_messages' in voicemail:
        voicemail['max_messages'] = int(voicemail['max_messages'])

    for key in ['attach_audio', 'delete_messages', 'ask_password']:
        if key in voicemail:
            voicemail[key] = (voicemail[key] == 'true')

    return voicemail


@step(u'When I request voicemail with id "([^"]*)"')
def when_i_request_voicemail_with_id_group1(step, voicemail_id):
    world.response = voicemail_ws.get_voicemail(voicemail_id)


@step(u'When I send a request for the voicemail with number "([^"]*)", using its id')
def when_i_send_a_request_for_the_voicemail_with_number_group1_using_its_id(step, number):
    voicemail_id = voicemail_helper.find_voicemail_id_with_number(number)
    world.response = voicemail_ws.get_voicemail(voicemail_id)


@step(u'Then the voicemail has the following parameters:')
def then_the_voicemail_has_the_following_parameters(step):
    expected_voicemail = _extract_voicemail_info(step.hashes[0])
    voicemail = world.response.data

    assert_that(voicemail, has_entries(expected_voicemail))


@step(u'When I request the list of voicemails$')
def when_i_request_the_list_of_voicemails(step):
    world.response = voicemail_ws.voicemail_list()


@step(u'When I request the list of voicemails with the following parameters:')
def when_i_request_the_list_of_voicemails_with_the_following_parameters(step):
    parameters = step.hashes[0]
    world.response = voicemail_ws.voicemail_list(parameters)


@step(u'Then I get a list containing the following voicemails:')
def then_i_get_a_list_containing_the_following_voicemails(step):
    assert_that(world.response.data, has_entries(
        'total', instance_of(int),
        'items', instance_of(list)))

    voicemail_list = world.response.data['items']

    for voicemail in step.hashes:
        voicemail = _extract_voicemail_info(voicemail)
        assert_that(voicemail_list, has_item(has_entries(voicemail)))


@step(u'Then I get a list of voicemails in the following order:')
def then_i_get_a_list_of_voicemails_in_the_following_order(step):
    all_voicemails = world.response.data['items']
    expected_voicemails = [_extract_voicemail_info(v) for v in step.hashes]
    assert_has_dicts_in_order(all_voicemails, expected_voicemails)


@step(u'Then I have a list with (\d+) of (\d+) results')
def then_i_have_a_list_with_n_of_n_results(step, nb_list, nb_total):
    nb_list = int(nb_list)
    nb_total = int(nb_total)
    assert_that(world.response.data, all_of(
        has_entry('total', equal_to(nb_total)),
        has_entry('items', has_length(nb_list))))


@step(u'Then I have a list with (\d+) results$')
def then_i_have_a_list_with_n_results(step, nb_list):
    nb_list = int(nb_list)
    assert_that(world.response.data, has_entry('items', has_length(nb_list)))


@step(u'Then the list contains the same total voicemails as on the server')
def then_the_list_contains_the_same_total_voicemails_as_on_the_server(step):
    total_server = voicemail_helper.total_voicemails()
    total_response = world.response.data['total']
    assert_that(total_server, equal_to(total_response))


@step(u'Then I do not have the following voicemails in the list:')
def then_i_dot_not_have_the_following_voicemails_in_the_list(step):
    all_voicemails = world.response.data['items']
    not_expected_voicemails = [_extract_voicemail_info(v) for v in step.hashes]

    assert_does_not_have_any_dicts(all_voicemails, not_expected_voicemails)
