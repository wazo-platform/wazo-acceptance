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

from hamcrest import assert_that, equal_to, has_item, has_entry, has_length, has_entries, is_not
from lettuce import step, world

from xivo_acceptance.action.webi import user as user_action_webi
from xivo_acceptance.action.restapi import func_key_action_restapi
from xivo_acceptance.helpers import extension_helper
from xivo_acceptance.helpers import func_key_helper
from xivo_acceptance.helpers import group_helper
from xivo_acceptance.helpers import meetme_helper
from xivo_acceptance.helpers import queue_helper
from xivo_acceptance.helpers import user_helper
from xivo_lettuce.xivo_hamcrest import assert_has_dicts_in_order
from xivo_lettuce import common


@step(u'Given there is no func key with id "([^"]*)"')
def given_there_is_no_func_key_with_id_group1(step, func_key_id):
    func_key_helper.delete_func_key(func_key_id)


@step(u'When I request the func key with id "([^"]*)" via RESTAPI')
def when_i_request_the_func_key_with_id_group1_via_restapi(step, func_key_id):
    world.response = func_key_action_restapi.get_func_key(func_key_id)


@step(u'When I request the funckey with a destination for user "([^"]*)" "([^"]*)"')
def when_i_request_the_funckey_with_a_destination_for_user_group1_group2(step, firstname, lastname):
    user = user_helper.get_by_firstname_lastname(firstname, lastname)
    func_key_ids = func_key_helper.find_func_keys_with_user_destination(user.id)
    assert_that(func_key_ids, has_length(1), "More than one func key with the same destination")

    world.response = func_key_action_restapi.get_func_key(func_key_ids[0])


@step(u'When I request the list of func keys via RESTAPI')
def when_i_request_the_list_of_func_keys_via_restapi(step):
    world.response = func_key_action_restapi.func_key_list()


@step(u'When I request the list of func keys with the following parameters via RESTAPI:')
def when_i_request_the_list_of_func_keys_with_the_following_parameters_via_restapi(step):
    parameters = step.hashes[0]
    world.response = func_key_action_restapi.func_key_list(parameters)


@step(u'Then the user "([^"]*)" has the following func keys:')
def then_the_user_group1_has_the_following_func_keys(step, user):
    common.open_url('user', 'search', {'search': user})
    common.edit_line(user)
    common.go_to_tab('Func Keys')
    for line_number, line in enumerate(step.hashes, 1):
        _check_func_key(line, line_number)


def _check_func_key(info, line_number):
    line = user_action_webi.find_func_key_line(line_number)

    key_num = info['Key']
    key_type = info['Type']
    key_label = info['Label']
    key_destination = info['Destination']
    key_supervision = info['Supervision']

    key_num_field = user_action_webi.find_key_number_field(line)
    value = _extract_dropdown_value(key_num_field)
    assert_that(value, equal_to(key_num), "func key num differs (%s instead of %s)" % (value, key_num))

    key_type_field = user_action_webi.find_key_type_field(line)
    value = _extract_dropdown_value(key_type_field)
    assert_that(value, equal_to(key_type), "func key type differs (%s instead of %s)" % (value, key_type))

    destination_value = _extract_destination_value(key_type, line)
    assert_that(destination_value, equal_to(key_destination), "func key destination differs (%s instead of %s)" % (value, key_destination))

    key_label_field = user_action_webi.find_key_label_field(line)
    value = key_label_field.get_attribute('value')
    assert_that(value, equal_to(key_label), "func key label differs (%s instead of %s)" % (value, key_label))

    key_supervision_field = user_action_webi.find_key_supervision_field(line)
    value = _extract_dropdown_value(key_supervision_field)
    assert_that(value, equal_to(key_supervision), "func key supervision differs (%s instead of %s)" % (value, key_supervision))


def _extract_dropdown_value(dropdown):
    return dropdown.first_selected_option.text


def _extract_destination_value(key_type, line):
    key_destination_field = user_action_webi.find_key_destination_field(key_type, line)
    if key_type == 'Filtering Boss - Secretary':
        value = _extract_dropdown_value(key_destination_field)
    else:
        value = key_destination_field.get_attribute('value')

    return value


@step(u'Then the list contains the following func keys:')
def then_the_list_contains_the_following_func_keys(step):
    func_keys = _map_func_keys_with_destination_name(world.response.data['items'])
    for func_key in step.hashes:
        assert_that(func_keys, has_item(has_entries(func_key)))


@step(u'Then the list does not contain the following func keys:')
def then_the_list_does_not_contain_the_following_func_keys(step):
    func_keys = _map_func_keys_with_destination_name(world.response.data['items'])
    for func_key in step.hashes:
        assert_that(func_keys, is_not(has_item(has_entries(func_key))))


@step(u'Then the list contains the following func keys in the right order:')
def then_the_list_contains_the_following_func_keys_in_the_right_order(step):
    func_keys = _map_func_keys_with_destination_name(world.response.data['items'])
    expected_func_keys = [f for f in step.hashes]
    assert_has_dicts_in_order(func_keys, expected_func_keys)


@step(u'Then the list only contains "([^"]*)" func keys destination "([^"]*)"')
def then_the_list_only_contains_func_keys_destination_service(step, expected_count, destination_type):
    count = 0
    for func_key in world.response.data['items']:
        if func_key['destination'] == destination_type:
            count += 1
    assert_that(count, equal_to(int(expected_count)))


def _map_func_keys_with_destination_name(func_keys):
    converted = []
    for func_key in func_keys:
        converted.append({
            'type': func_key['type'],
            'destination': func_key['destination'],
            'destination name': _find_destination_name(func_key)})

    return converted


def _find_destination_name(func_key):
    destination = func_key['destination']

    if destination == 'user':
        return _find_user_name_for_func_key(func_key)
    elif destination == 'group':
        return _find_group_name_for_func_key(func_key)
    elif destination == 'queue':
        return _find_queue_name_for_func_key(func_key)
    elif destination == 'conference':
        return _find_meetme_name_for_func_key(func_key)
    elif destination == 'service':
        return _find_extension_name_for_func_key(func_key)


def _find_user_name_for_func_key(func_key):
    user = user_helper.get_by_user_id(func_key['destination_id'])
    return "%s %s" % (user.firstname, user.lastname)


def _find_group_name_for_func_key(func_key):
    group = group_helper.get_group(func_key['destination_id'])
    return group.name


def _find_queue_name_for_func_key(func_key):
    queue = queue_helper.find_queue_with_id(func_key['destination_id'])
    return queue.name


def _find_meetme_name_for_func_key(func_key):
    meetme = meetme_helper.find_meetme_with_id(func_key['destination_id'])
    return meetme.name


def _find_extension_name_for_func_key(func_key):
    extension = extension_helper.get_extension(func_key['destination_id'])
    return extension.typeval


@step(u'Then I get a func key of type "([^"]*)"')
def then_i_get_a_func_key_of_type_group1(step, func_key_type):
    assert_that(world.response.data, has_entry('type', func_key_type))


@step(u'Then I get a func key with a destination id for user "([^"]*)" "([^"]*)"')
def then_i_get_a_func_key_with_a_destination_id_for_user_group1_group2(step, firstname, lastname):
    destination_id = world.response.data['destination_id']
    user = user_helper.get_by_firstname_lastname(firstname, lastname)
    assert_that(user.id, equal_to(destination_id))
