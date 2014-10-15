# -*- coding: utf-8 -*-

# Copyright (C) 2013-2014 Avencall
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

from hamcrest import assert_that, has_item
from hamcrest.core.base_matcher import BaseMatcher
from lettuce import step

from xivo_acceptance.helpers import confd_requests_helper


@step(u'Then the confd REST API received a request with infos:$')
def then_the_confd_rest_api_received_a_request_with_infos(step):
    last_requests = confd_requests_helper.last_requests_infos()
    for expected_request_infos in step.hashes:
        assert_that(last_requests, has_item(has_request_infos(expected_request_infos)))


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
