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

import re

from lettuce import step, world
from hamcrest import *


@step(u'Then I get an empty list$')
def then_i_get_an_empty_list(step):
    user_response = world.response.data
    assert_that(user_response, has_entry('total', 0))
    assert_that(user_response, has_entry('items', []))


@step(u'Then I get a response with status "([^"]*)"$')
def then_i_get_a_response_with_status_group1(step, status):
    status_code = int(status)
    error_msg = "response received: %s" % world.response.data
    assert_that(world.response.status, equal_to(status_code), error_msg)


@step(u'Then I get a response with an id$')
def then_i_get_a_response_with_an_id(step):
    assert_that(world.response.data, has_entry('id', instance_of(int)))


@step(u'Then I get an error message "([^"]*)"$')
def then_i_get_an_error_message_group1(step, error_message):
    assert_that(world.response.data, has_item(error_message))


@step(u'Then I get an error message matching "([^"]*)"$')
def then_i_get_an_error_message_matching_group1(step, regex):
    messages = world.response.data
    has_match = _check_for_regex_match(messages, regex)
    assert_that(has_match, "regex '%s' did not match any message. Messages: %s" % (regex, messages))


def _check_for_regex_match(messages, regex):
    for message in messages:
        if re.search(regex, message):
            return True
    return False


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


@step(u'Then I get a response with the following link resources:')
def then_i_get_a_response_with_the_following_link_resources(step):
    for resource_info in step.hashes:
        resource = resource_info['resource']
        resource_id = resource_info['id']
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
