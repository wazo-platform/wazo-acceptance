# -*- coding: utf-8 -*-
# Copyright 2013-2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from lettuce import step

from xivo_acceptance.helpers import schedule_helper, user_helper


@step(u'Given I have a schedule "([^"]*)" in "([^"]*)" with the following schedules:')
def given_i_have_a_schedule_group1_in_group2_with_the_following_schedules(step, name, timezone):
    schedule_helper.add_schedule(name, timezone, step.hashes)


@step(u'Given I have a schedule "([^"]*)" in "([^"]*)" towards user "([^"]*)" "([^"]*)" with the following schedules:')
def given_i_have_a_schedule_group1_in_group2_towards_user_group3_group4_with_the_following_schedules(step, name, timezone, firstname, lastname):
    user_id = user_helper.get_user_by_name('{} {}'.format(firstname, lastname))
    destination = {'type': 'user', 'user_id': user_id}
    schedule_helper.add_schedule(name, timezone, step.hashes, destination)


@step(u'Given there are schedules:')
def given_there_are_schedules(step):
    for data in step.hashes:
        schedule_helper.add_or_replace_schedule(data)
