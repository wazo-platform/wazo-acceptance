# -*- coding: utf-8 -*-
# Copyright 2013-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from hamcrest import assert_that
from hamcrest import has_items
from lettuce import step
from xivo_acceptance.helpers import line_read_helper
from xivo_acceptance.lettuce import asterisk, common


@step(u'Given the AMI is monitored')
def given_the_ami_is_monitored(step):
    asterisk.start_ami_monitoring()


@step(u'Then I see in the AMI that the line "([^"]*)@(\w+)" has been synchronized')
def then_i_see_in_the_ami_that_the_line_group1_has_been_synchronized(step, extension, context):
    line = line_read_helper.find_with_exten_context(extension, context)
    line_name = line['name']
    lines = [
        'Action: PJSIPNotify',
        'Endpoint: {}'.format(line_name),
        'Variable: Event=check-sync',
    ]

    def _assert():
        ami_lines = asterisk.fetch_ami_lines()
        assert_that(ami_lines, has_items(*lines))

    common.wait_until_assert(_assert, tries=3)
