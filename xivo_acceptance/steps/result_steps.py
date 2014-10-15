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

import re

from lettuce import step, world
from hamcrest import assert_that, equal_to, has_item, has_entry, is_not, has_key, instance_of, ends_with, has_entries, has_length


@step(u'When I memorize the first entry in the list')
def when_i_memorize_the_first_entry_in_the_list(step):
    world.list_entry = world.response.data['items'][0]


@step(u'Then the memorized entry is not in the list')
def then_the_memorized_entry_is_not_in_the_list(step):
    assert_that(world.response.data, has_key('items'), "did not receive any list from CONFD")

    items = world.response.data['items']
    assert_that(items, is_not(has_item(world.list_entry)))


@step(u'Then I get an empty list$')
def then_i_get_an_empty_list(step):
    user_response = world.response.data
    assert_that(user_response, has_entry('total', 0))
    assert_that(user_response, has_entry('items', []))


@step(u'Then I get a response with status "([^"]*)"$')
def then_i_get_a_response_with_status_group1(step, status):
    status_code = int(status)
    world.response.check_status(status_code)


@step(u'Then I get a response with an id$')
def then_i_get_a_response_with_an_id(step):
    assert_that(world.response.data, has_entry('id', instance_of(int)))


@step(u'Then I get an error message "([^"]*)"$')
def then_i_get_an_error_message_group1(step, error_message):
    assert_that(world.response.data, has_item(error_message))


@step(u'Then I get an error message matching "([^"]*)"$')
def then_i_get_an_error_message_matching_group1(step, regex):
    world.response.check_regex(regex)


@step(u'Then I get a header with a location for the "([^"]*)" resource$')
def then_i_get_a_header_with_a_location_for_the_group1_resource(step, resource):
    resource_id = world.response.data['id']
    expected_location = '/1.1/%s/%s' % (resource, resource_id)

    assert_that(world.response.headers, has_entry('location', ends_with(expected_location)))


@step(u'Then I get a header with a location matching "([^"]*)"$')
def then_i_get_a_header_with_a_location_matching_group1(step, regex):
    assert_that(world.response.headers, has_key('location'))
    location = world.response.headers['location']

    matches = re.search(regex, location) is not None
    assert_that(matches, "regex '%s' did not match location header. Location: %s" % (regex, location))


@step(u'Then I get a response with a link to the "([^"]*)" resource$')
def then_i_get_a_response_with_a_link_to_an_extension_resource(step, resource):
    resource_id = world.response.data['id']
    assert_response_has_resource_link(resource, resource_id)


@step(u'Then I get a response with a link to the "([^"]*)" resource with id "([^"]*)"$')
def then_i_get_a_response_with_a_link_to_a_resource_with_id(step, resource, resource_id):
    assert_response_has_resource_link(resource, resource_id)


@step(u'Then I get a response with a link to the "([^"]*)" resource using the id "([^"]*)"$')
def then_i_get_a_response_with_a_link_to_a_resource_with_id_using_the_id(step, resource, resource_key):
    resource_id = world.response.data[resource_key]
    assert_response_has_resource_link(resource, resource_id)


def assert_response_has_resource_link(resource, resource_id):
    expected_url = _build_resource_url(resource, resource_id)
    assert_that(world.response.data, _has_link_entry(resource, expected_url))


def _build_resource_url(resource, resource_id):
    host = world.config.xivo_host
    port = world.config.rest_port
    expected_url = "https://%s:%s/1.1/%s/%s" % (host, port, resource, resource_id)
    return expected_url


def _has_link_entry(resource, url):
    return has_entry(u'links', has_item(
        has_entries({
            u'rel': resource,
            u'href': url})))


@step(u'Then each item has a "([^"]*)" link using the id "([^"]*)"')
def then_each_item_has_a_group1_link_using_the_id_group2(step, resource, resource_key):
    items = world.response.data['items']
    assert_that(items, is_not(has_length(0)))

    for item in items:
        assert_that(item, has_key(resource_key))

        resource_id = item[resource_key]
        expected_url = _build_resource_url(resource, resource_id)
        assert_that(item, _has_link_entry(resource, expected_url))


@step(u'Then I get a list with (\d+) of (\d+) items')
def then_i_get_a_list_with_1_of_1_items(step, expected_items, expected_total):
    expected_items = int(expected_items)
    expected_total = int(expected_total)

    nb_items = len(world.response.data['items'])
    total = world.response.data['total']

    assert_that(nb_items, equal_to(expected_items))
    assert_that(total, equal_to(expected_total))
