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

from hamcrest import assert_that, has_entries
from lettuce import step

from xivo_acceptance.action.webi import meetme as meetme_action_webi
from xivo_acceptance.helpers import meetme_helper, cti_helper
from xivo_lettuce import common


@step(u'Given there is no conference with number "([^"]*)"')
def given_there_is_no_conference_with_number(step, conf_number):
    meetme_helper.delete_meetme_with_confno(conf_number)


@step(u'Given there are the following conference rooms:')
def given_there_are_the_following_conference_rooms(step):
    for meetme in step.hashes:
        meetme_action_webi.add_or_replace_meetme(meetme)


@step(u'When I delete the conference room with number "([^"]*)"')
def when_i_delete_the_conference_room_with_number_group1(step, conf_number):
    meetme_helper.delete_meetme_with_confno(conf_number)


@step(u'When I add the following conference rooms:')
def when_i_add_the_following_conference_rooms(step):
    for meetme in step.hashes:
        meetme_action_webi.add_or_replace_meetme(meetme)


@step(u'When I update the following conference rooms:')
def when_i_update_the_following_conference_rooms(step):
    for meetme in step.hashes:
        meetme_action_webi.update_meetme(meetme)


@step(u'Then the following conference rooms appear in the conference room xlet:')
def then_the_following_conference_rooms_appear_in_the_list(step):
    res = cti_helper.get_conference_room_infos()
    for src_dict, expected_dict in zip(res['return_value']['content'], step.hashes):
        assert_that(src_dict, has_entries(expected_dict))


@step(u'Then I see the conference room "([^"]*)" exists$')
def then_i_see_the_element_exists(step, name):
    common.open_url('meetme')
    line = common.find_line(name)
    assert line is not None, 'conference room: %s does not exist' % name


@step(u'Then I see the conference room "([^"]*)" not exists$')
def then_i_see_the_element_not_exists(step, name):
    common.open_url('meetme')
    line = common.find_line(name)
    assert line is None, 'conference room: %s exist' % name
