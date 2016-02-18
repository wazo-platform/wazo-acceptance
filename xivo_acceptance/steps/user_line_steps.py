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

from hamcrest import assert_that, equal_to, is_not, none
from lettuce import step, world

from xivo_acceptance.action.confd import user_line_action_confd
from xivo_acceptance.helpers import user_helper, line_sip_helper


@step(u'Given SIP line "([^"]*)" is associated to user "([^"]*)" "([^"]*)"')
def given_sip_line_group1_is_associated_to_user_group2_group3(step, sip_username, firstname, lastname):
    line = line_sip_helper.find_by_username(sip_username)
    assert_that(line, is_not(none()), "Line with username {} not found".format(sip_username))
    user_id = user_helper.get_user_id_with_firstname_lastname(firstname, lastname)
    world.response = user_line_action_confd.create_user_line(user_id, {'line_id': line['id']})
    assert_that(world.response.status, equal_to(201), unicode(world.response.data))
