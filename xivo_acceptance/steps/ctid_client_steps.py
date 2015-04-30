# -*- coding: utf-8 -*-

# Copyright (C) 2015 Avencall
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

from lettuce import step, world
from hamcrest import assert_that, equal_to, calling, raises
from requests.exceptions import HTTPError

from xivo_ctid_client import Client

from xivo_acceptance.helpers import line_helper
from xivo_acceptance.helpers import user_helper
from xivo_acceptance.helpers import xivo_helper


def _find_user_id(info):
    return user_helper.get_user_id_with_firstname_lastname(info['firstname'], info['lastname'])


def _find_line_id(info):
    exten = info['number']
    context = info['context']
    return int(line_helper.find_line_id_with_exten_context(exten, context))


@step(u'Then I should have the following user status when I query the cti:')
def then_i_should_have_have_the_following_user_status_when_i_query_the_cti(step):
    c = Client(host=world.config['xivo_host'])

    uuid = xivo_helper.get_uuid()
    for info in step.hashes:
        user_id = _find_user_id(info)
        expected = {
            u'origin_uuid': uuid,
            u'id': user_id,
            u'presence': info['presence'],
        }

        assert_that(c.users.get(user_id), equal_to(expected))


@step(u'Then I should have the following endpoint status when I query the cti:')
def then_i_should_have_have_the_following_endpoint_status_when_i_query_the_cti(step):
    c = Client(host=world.config['xivo_host'])

    uuid = xivo_helper.get_uuid()
    for info in step.hashes:
        line_id = _find_line_id(info)
        expected = {
            u'origin_uuid': uuid,
            u'id': line_id,
            u'status': int(info['status']),
        }

        assert_that(c.endpoints.get(line_id), equal_to(expected))


@step(u'Then I should have a "([^"]*)" when I search for endpoint "([^"]*)" on the cti http interface')
def then_i_should_have_a_group1_when_i_search_for_endpoint_group2_on_the_cti_http_interface(step, status_code, endpoint_id):
    c = Client(host=world.config['xivo_host'])

    assert_that(
        calling(c.endpoints.get).with_args(int(endpoint_id)),
        raises(HTTPError, r"^{}".format(status_code)))


@step(u'Then I should have a "([^"]*)" when I search for user "([^"]*)" on the cti http interface')
def then_i_should_have_a_group1_when_i_search_for_user_group2_on_the_cti_http_interface(step, status_code, user_id):
    c = Client(host=world.config['xivo_host'])

    assert_that(
        calling(c.users.get).with_args(int(user_id)),
        raises(HTTPError, r"^{}".format(status_code)))


@step(u'When I query the infos URL on the cti http interface, I receive the uuid')
def when_i_query_the_infos_url_on_the_cti_http_interface_i_receive_the_uuid(step):
    c = Client(host=world.config['xivo_host'])

    uuid = xivo_helper.get_uuid()

    assert_that(c.infos.get(), equal_to({'uuid': uuid}))
