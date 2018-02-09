# -*- coding: utf-8 -*-
# Copyright 2016-2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from lettuce import step, world
from hamcrest import (
    assert_that,
    has_item,
)

_FAIL2BAN_REGEX_ARGS = {
    'xivo-provd': {
        'log': '/var/log/xivo-provd-fail2ban.log',
        'regex': '/etc/fail2ban/filter.d/xivo-provd.conf',
    },
}


@step(u'Then fail2ban-regex for "([^"]*)" matches (\d+) lines')
def given_a_update_plugins_provd(step, name, match_count):
    match_count = int(match_count)
    args = _FAIL2BAN_REGEX_ARGS[name]
    command = ['fail2ban-regex', args['log'], args['regex']]

    output = world.ssh_client_xivo.out_call(command)
    last_lines = output.splitlines()[-5:]

    expected_line = 'Lines: {0} lines, 0 ignored, {0} matched, 0 missed'.format(match_count)
    assert_that(last_lines, has_item(expected_line),
                'output did not match: command was {}'.format(command))
