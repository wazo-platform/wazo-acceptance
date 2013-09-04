# -*- coding: utf-8 -*-

# Copyright (C) 2013 Avencall
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

import re
from hamcrest import assert_that, is_not, none
from xivo_lettuce import sysutils


def assert_last_request_matches(action, query):
    last_request = _get_last_request()
    request_pattern = '.*https?://.*%s\?%s' % (action, query)
    result = re.match(request_pattern, last_request)

    assert_that(result, is_not(none()))


def _get_last_request():
    last_line = sysutils.output_command(['tail', '-n', '1', '/var/log/xivo-restapid.log'])
    return last_line
