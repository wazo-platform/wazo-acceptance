# -*- coding: utf-8 -*-
# Copyright (C) 2013-2016 Avencall
# SPDX-License-Identifier: GPL-3.0-or-later

from hamcrest import assert_that, has_entries, has_item
from lettuce import step

from xivo_acceptance.action.webi import meetme as meetme_action_webi
from xivo_acceptance.helpers import meetme_helper, cti_helper
from xivo_acceptance.lettuce import common


@step(u'Given there is no conference with number "([^"]*)"')
def given_there_is_no_conference_with_number(step, conf_number):
    meetme_helper.delete_meetme_with_confno(conf_number)


@step(u'Given there are the following conference rooms:')
def given_there_are_the_following_conference_rooms(step):
    for meetme in step.hashes:
        meetme_action_webi.add_or_replace_meetme(meetme)


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
    actual_conf_rooms = cti_helper.get_conference_room_infos()['return_value']['content']
    for expected_conf_room in step.hashes:
        assert_that(actual_conf_rooms, has_item(has_entries(expected_conf_room)))


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
