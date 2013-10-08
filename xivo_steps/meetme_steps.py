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

from hamcrest import assert_that, has_entries
from lettuce import step

from xivo_acceptance.helpers import meetme_helper, cti_helper
from xivo_lettuce.manager_webi import meetme_manager


@step(u'Given there are no conference rooms')
def given_there_are_no_conference_rooms(step):
    meetme_helper.delete_all_meetmes()


@step(u'When I add the following conference rooms:')
def when_i_add_the_following_conference_rooms(step):
    for meetme in step.hashes:
        meetme_manager.create_meetme(meetme)


@step(u'When I update the following conference rooms:')
def when_i_update_the_following_conference_rooms(step):
    for meetme in step.hashes:
        meetme_manager.update_meetme(meetme)


@step(u'Then the following conference rooms appear in the conference room xlet:')
def then_the_following_conference_rooms_appear_in_the_list(step):
    res = cti_helper.get_conference_room_infos()
    for src_dict, expected_dict in zip(res['return_value']['content'], step.hashes):
        assert_that(src_dict, has_entries(expected_dict))
