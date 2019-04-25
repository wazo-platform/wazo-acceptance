# -*- coding: utf-8 -*-
# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import re

from hamcrest import (
    assert_that,
    is_not,
    none,
)
from lettuce import step

from xivo_acceptance.lettuce import sysutils


@step(u'Then the mirror list contains a line matching "([^"]*)"')
def then_the_mirror_list_contains_a_line_matching_group1(step, regex):
    match = _match_on_mirror_list(regex)
    assert_that(match, is_not(none()))


def _match_on_mirror_list(regex):
    output = sysutils.output_command(['apt-cache', 'policy'])
    return re.search(regex, output)
