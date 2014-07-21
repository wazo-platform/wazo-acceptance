# -*- coding: utf-8 -*-

# Copyright (C) 2014 Avencall
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

import json

from lettuce import step, world
from hamcrest import assert_that, has_item, has_entries

from xivo_acceptance.helpers import user_helper
from xivo_acceptance.helpers import extension_helper
from xivo_acceptance.helpers import voicemail_helper
from xivo_acceptance.helpers import device_helper

from xivo_lettuce.xivo_hamcrest import assert_has_dicts_in_order, assert_does_not_have_any_dicts


@step(u'Given I have the following "([^"]*)":')
def given_i_have_the_following_group1(step, resource):
    for item in _convert_to_items(step.hashes):
        _delete_similar_resources(resource, item)
        _create_resource(resource, item)


@step(u'When I request a list for "([^"]*)" using parameters:')
def when_i_request_a_list_for_group1_using_parameters(step, resource):
    parameters = _convert_parameters(step.hashes)
    world.response = world.restapi_utils_1_1.rest_get(resource, params=parameters)


@step(u'Then I get a response (\d+) matching "([^"]*)"')
def then_i_get_a_response_status_matching_group1(step, status, regex):
    status = int(status)

    world.response.check_status(status)
    world.response.check_regex(regex)


@step(u'When I POST at "([^"]*)":')
def when_i_post_at_group1(step, url):
    document = json.loads(step.multiline)
    world.response = world.restapi_utils_1_1.rest_post(url, document)


@step(u'Then I get a list containing the following items:')
def then_i_get_a_list_containing_the_following_items(step):
    items = world.response.items()

    for item in _convert_to_items(step.hashes):
        assert_that(items, has_item(has_entries(item)))


@step(u'Then I get a list that does not contain the following items:')
def then_i_get_a_list_that_does_not_contain_the_following_items(step):
    expected_items = _convert_to_items(step.hashes)
    items = world.response.items()
    assert_does_not_have_any_dicts(items, expected_items)


@step(u'Then I get a list of items in the following order:')
def then_i_get_a_list_of_items_in_the_following_order(step):
    expected_items = _convert_to_items(step.hashes)
    items = world.response.items()
    assert_has_dicts_in_order(items, expected_items)


def _convert_to_items(hashes):
    return [json.loads(h['item']) for h in hashes]


def _convert_parameters(hashes):
    return {h['name']: h['value'] for h in hashes}


def _delete_similar_resources(resource, item):
    if resource == "users":
        user_helper.delete_similar_users(item)
    elif resource == "extensions":
        extension_helper.delete_similar_extensions(item)
    elif resource == "voicemails":
        voicemail_helper.delete_similar_voicemails(item)
    elif resource == "devices":
        device_helper.delete_similar_devices(item)
    else:
        raise NotImplementedError("delete for resource '%s' not implemented" % resource)


def _create_resource(resource, item):
    response = world.restapi_utils_1_1.rest_post(resource, item)
    response.check_status()
