# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import re

from hamcrest import (
    assert_that,
    is_not,
    none,
)
from behave import then

from .. import sysutils


@then(u'the mirror list contains a line matching "{mirror}"')
def then_the_mirror_list_contains_a_line_matching_mirror(context, mirror):
    match = _match_on_mirror_list(context, mirror)
    assert_that(match, is_not(none()))


def _match_on_mirror_list(context, regex):
    output = sysutils.output_command(context, ['apt-cache', 'policy'])
    return re.search(regex, output)
