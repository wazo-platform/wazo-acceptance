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
from hamcrest import assert_that, equal_to

from xivo_ctid_client import Client

from xivo_acceptance.helpers import user_helper
from xivo_acceptance.helpers import xivo_helper


def _find_user_id(info):
    return user_helper.find_user_id_with_firstname_lastname(info['firstname'], info['lastname'])


@step(u'Then I should have have the following user status when I query the cti:')
def then_i_should_have_have_the_following_user_status_when_i_query_the_cti(step):
    c = Client(host=world.config['xivo_host'])

    uuid = xivo_helper.get_uuid()
    for info in step.hashes:
        user_id = _find_user_id(info)
        expected = {
            'origin_uuid': uuid,
            'id': user_id,
            'presence': info['presence'],
        }

        assert_that(c.users.get(user_id), equal_to(expected))


@step(u'Then I should have a "([^"]*)" when I search for user "([^"]*)" on the cti http interface')
def then_i_should_have_a_group1_when_i_search_for_user_group2_on_the_cti_http_interface(step, status_code, user_id):
    c = Client(host=world.config['xivo_host'])

    try:
        c.users.get(int(user_id))
    except Exception as e:
        assert_that(str(e).startswith(status_code))
