# Copyright 2016-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from behave import then
from hamcrest import (
    assert_that,
    has_item,
)

_FAIL2BAN_REGEX_ARGS = {
    'wazo-provd': {
        'log': '/var/log/wazo-provd-fail2ban.log',
        'regex': '/etc/fail2ban/filter.d/wazo-provd.conf',
    },
}


@then('fail2ban-regex for "{name}" matches {match_count} lines')
def then_fail2banregex_for_name_matches_x_lines(context, name, match_count):
    match_count = int(match_count)
    args = _FAIL2BAN_REGEX_ARGS[name]
    command = ['fail2ban-regex', args['log'], args['regex']]

    output = context.ssh_client.out_call(command)
    last_lines = output.splitlines()[-5:]

    expected_line = 'Lines: {0} lines, 0 ignored, {0} matched, 0 missed'.format(match_count)
    assert_that(last_lines, has_item(expected_line),
                f'output did not match: command was {command}')
