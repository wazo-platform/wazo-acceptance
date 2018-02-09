# -*- coding: utf-8 -*-
# Copyright (C) 2013-2014 Avencall
# SPDX-License-Identifier: GPL-3.0+

import re

from hamcrest import assert_that, has_item
from hamcrest.core.base_matcher import BaseMatcher
from lettuce import step

from xivo_acceptance.helpers import confd_requests_helper
from xivo_acceptance.lettuce import common


@step(u'Then the confd REST API received a request with infos:$')
def then_the_confd_rest_api_received_a_request_with_infos(step):
    def _assert():
        last_requests = confd_requests_helper.last_requests_infos()
        for expected_request_infos in step.hashes:
            assert_that(last_requests, has_item(has_request_infos(expected_request_infos)))

    common.wait_until_assert(_assert, tries=3)


def has_request_infos(expected_request_infos):
    return HasEntriesRegex(expected_request_infos)


class HasEntriesRegex(BaseMatcher):
    def __init__(self, expected_request_infos):
        self.expected_request_infos = expected_request_infos

    def _matches(self, item):
        test_passed = True
        for key, expected_value in self.expected_request_infos.iteritems():
            test_passed = test_passed and (re.match(expected_value, item[key]) is not None)

        return test_passed

    def describe_to(self, description):
        description.append_text('dict having entries matching').append_value(self.expected_request_infos)
