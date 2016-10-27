# -*- coding: utf-8 -*-

# Copyright (C) 2013-2016 Avencall
# Copyright (C) 2016 Proformatique Inc.
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

from lettuce import step
from lettuce.registry import world

from xivo_acceptance.helpers import cti_profile_helper, user_helper


@step(u'When I activate the CTI client for user "([^"]*)" "([^"]*)"$')
def when_i_activate_the_cti_client_for_user_group1_group2(step, firstname, lastname):
    user_helper.enable_cti_client(firstname, lastname)


@step(u'When I associate CTI profile with name "([^"]*)" with user "([^"]*)" "([^"]*)"')
def when_i_associate_cti_profile_with_name_group1_with_user_group2_group3(step, cti_profile_name, firstname, lastname):
    cti_profile_id = cti_profile_helper.get_id_with_name(cti_profile_name)
    user = user_helper.get_by_firstname_lastname(firstname, lastname)
    world.confd_client.users(user).add_cti_profile(cti_profile_id)
