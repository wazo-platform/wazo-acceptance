# -*- coding: utf-8 -*-
# Copyright 2013-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from hamcrest import assert_that
from hamcrest import has_entries
from lettuce import step, world
from xivo_acceptance.helpers.datetime_helper import close_to
from xivo_acceptance.lettuce import common


@step(u'Then I have the last call log matching:')
def then_i_have_the_last_call_log_matching(step):
    expected = dict(step.hashes[0])
    expected_duration = int(expected.pop('duration', None))
    if expected.get('answered'):
        expected['answered'] = bool(expected['answered'])

    def _assert():
        actual = world.call_logd_client.cdr.list(direction='desc', limit=1)['items'][0]
        assert_that(actual, has_entries(expected))
        if expected_duration:
            assert_that(actual['duration'], close_to(expected_duration, 2))

    common.wait_until_assert(_assert, tries=5)
