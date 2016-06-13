# -*- coding: utf-8 -*-

# Copyright (C) 2016 Avencall
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

from lettuce import step, world
from hamcrest import assert_that, equal_to

_FAIL2BAN_REGEX_ARGS = {
    'xivo-prod': {
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
    last_line = output.splitlines()[-1]

    expected_last_line = 'Lines: {0} lines, 0 ignored, {0} matched, 0 missed'.format(match_count)
    assert_that(last_line, equal_to(expected_last_line),
                'output did not match: command was {}'.format(command))
