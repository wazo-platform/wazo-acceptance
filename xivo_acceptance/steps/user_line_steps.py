# -*- coding: utf-8 -*-
# Copyright (C) 2013-2016 Avencall
# Copyright (C) 2016 Proformatique Inc.
# SPDX-License-Identifier: GPL-3.0-or-later

from hamcrest import assert_that, is_not, none
from lettuce import step, world

from xivo_acceptance.helpers import user_helper, line_read_helper


@step(u'Given SIP line "([^"]*)" is associated to user "([^"]*)" "([^"]*)"')
def given_sip_line_group1_is_associated_to_user_group2_group3(step, sip_username, firstname, lastname):
    line = line_read_helper.find_by_sip_username(sip_username)
    assert_that(line, is_not(none()), "Line with username {} not found".format(sip_username))
    user = user_helper.get_by_firstname_lastname(firstname, lastname)
    world.confd_client.users(user).add_line(line)
