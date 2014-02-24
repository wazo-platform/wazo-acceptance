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

from hamcrest import assert_that, equal_to, has_item
from lettuce import step, world

from xivo_acceptance.action.webi import user as user_action_webi
from xivo_acceptance.action.restapi import func_key_action_restapi
from xivo_acceptance.helpers import user_helper, func_key_helper
from xivo_lettuce import common
from xivo_lettuce.xivo_hamcrest import not_empty


@step(u'Given I have a speeddial func key for user "([^"]*)" "([^"]*)"')
def given_i_have_a_speeddial_func_key_for_user_group1_group2(step, firstname, lastname):
    user = user_helper.get_by_firstname_lastname(firstname, lastname)
    func_key_helper.create_speeddial_with_user_destination(user)


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


@step(u'Then the list contains a speeddial func key for user "([^"]*)" "([^"]*)"')
def then_the_list_contains_a_speeddial_func_key_for_user_group1(step, firstname, lastname):
    fullname = "%s %s" % (firstname, lastname)
    user_func_keys = _filter_user_func_keys(world.response)
    user_names = [_find_user_name_for_func_key(func_key) for func_key in user_func_keys]
    assert_that(user_names, has_item(fullname), "no func key configured for user %s was found" % fullname)


def _filter_user_func_keys(response):
    items = response.data['items']
    assert_that(items, not_empty())

    return [func_key for func_key in items if func_key['type'] == 'speeddial' and func_key['destination'] == 'user']


def _find_user_name_for_func_key(func_key):
    user = user_helper.get_by_user_id(func_key['destination_id'])
    return "%s %s" % (user.firstname, user.lastname)
