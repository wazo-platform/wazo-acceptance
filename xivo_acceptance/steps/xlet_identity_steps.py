# -*- coding: utf-8 -*-
# Copyright (C) 2013-2015 Avencall
# SPDX-License-Identifier: GPL-3.0-or-later

from hamcrest import assert_that, is_not, equal_to, is_
from lettuce import step, world


@step(u'Then the Xlet identity shows name as "([^"]*)" "([^"]*)"')
def then_the_xlet_identity_shows_name_as_1_2(step, firstname, lastname):
    assert world.xc_identity_infos['fullname'] == '%s %s' % (firstname, lastname)


@step(u'Then the Xlet identity shows a voicemail "([^"]*)"')
def then_the_xlet_identity_shows_a_voicemail_1(step, vm_number):
    assert_that(world.xc_identity_infos['voicemail_num'], is_not(equal_to('')))
    assert_that(world.xc_identity_infos['voicemail_button'], is_(True))


@step(u'Then the Xlet identity shows an agent')
def then_the_xlet_identity_shows_an_agent_1(step):
    assert_that(world.xc_identity_infos['agent_button'], is_(True))


@step(u'Then the Xlet identity does not show any agent')
def then_the_xlet_identity_does_not_show_any_agent(step):
    assert_that(world.xc_identity_infos['agent_button'], is_(False))
