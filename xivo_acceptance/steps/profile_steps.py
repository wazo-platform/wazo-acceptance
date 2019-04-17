# -*- coding: utf-8 -*-
# Copyright 2013-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from hamcrest import assert_that, has_item
from lettuce import step

from xivo_acceptance.helpers import cti_helper


@step(u'Given there is a profile "([^"]*)" with no services and xlets:')
def given_there_is_a_profile_1_with_no_services_and_xlets(step, profile_name):
    pass


@step(u'When I add Xlet "([^"]*)" to profile "([^"]*)"')
def when_i_add_xlet_to_profile(step, xlet_name, profile_name):
    pass


@step(u'When I add the CTI profile "([^"]*)"')
def when_i_add_the_cti_profile_1(step, profile_name):
    pass


@step(u'Then I can\'t remove profile "([^"]*)"')
def then_i_see_errors(step, profile_label):
    pass


@step(u'Then I don\'t see xlet "([^"]*)"')
def then_i_don_t_see_xlet_group1(step, xlet):
    res = cti_helper.get_xlets()
    assert_that(res['xlets'], not has_item(xlet))


@step(u'Then I see xlet "([^"]*)"')
def then_i_see_xlet_group1(step, xlet):
    res = cti_helper.get_xlets()
    assert_that(res['xlets'], has_item(xlet))
