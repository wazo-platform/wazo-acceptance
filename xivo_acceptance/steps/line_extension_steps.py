# -*- coding: utf-8 -*-
# Copyright (C) 2013-2016 Avencall
# Copyright (C) 2016 Proformatique Inc.
# SPDX-License-Identifier: GPL-3.0+

from hamcrest import assert_that, is_not, none

from lettuce import step, world
from xivo_acceptance.helpers import extension_helper
from xivo_acceptance.helpers import line_read_helper


@step(u'Given SIP line "([^"]*)" is associated to extension "(\d+)@([\w_-]+)"')
def given_line_with_username_group1_is_associated_to_extension_group2(step, username, exten, context):
    line = line_read_helper.find_by_sip_username(username)
    assert_that(line, is_not(none()), "Line with username {} not found".format(username))
    extension = extension_helper.find_extension_by_exten_context(exten, context)
    assert_that(extension, is_not(none()), "Extension {}@{} not found".format(exten, context))
    world.confd_client.lines(line['id']).add_extension(extension)
