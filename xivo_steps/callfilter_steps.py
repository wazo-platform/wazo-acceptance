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

from lettuce import step

from xivo_acceptance.action.webi import callfilter as callfilter_action_webi
from xivo_acceptance.action.webi import user as user_action_webi
from xivo_lettuce import common


@step(u'Given there is no callfilter "([^"]*)"$')
def given_there_is_no_callfilter(step, search):
    common.remove_element_if_exist('callfilter', search)


@step(u'^When I create a callfilter "([^"]*)" with a boss "([^"]*)" with a secretary "([^"]*)"$')
def given_there_are_users_with_infos(step, callfilter_name, boss, secretary):
    callfilter_action_webi.add_boss_secretary_filter(callfilter_name, boss, secretary)


@step(u'Given there is a callfilter "([^"]*)" with boss "([^"]*)" and secretary "([^"]*)"')
def given_there_is_a_callfilter_group1_with_boss_group2_and_secretary_group3(step, callfilter_name, boss, secretary):
    callfilter_action_webi.add_boss_secretary_filter(callfilter_name, boss, secretary)


@step(u'When I deactivate boss secretary filtering for user "([^"]*)"')
def when_i_deactivate_boss_secretary_filtering_for_user_group1(step, user):
    user_action_webi.deactivate_bsfilter(user)
