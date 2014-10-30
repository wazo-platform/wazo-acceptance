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

import hamcrest as h
import pprint


def assert_has_dicts_in_order(haystack, needles):
    msg = "haystack: %s" % pprint.pformat(haystack)
    filtered_needles = _filter_expected_needles(haystack, needles)
    h.assert_that(filtered_needles, h.contains(*_expected_needles(needles)), msg)


def _filter_expected_needles(haystack, needles):
    matcher = h.any_of(*_expected_needles(needles))
    return [v for v in haystack if matcher.matches(v)]


def _expected_needles(needles):
    matcher = []
    for needle in needles:
        matcher.append(h.has_entries(needle))
    return matcher


def assert_does_not_have_any_dicts(haystack, needles):
    for needle in needles:
        h.assert_that(haystack, h.is_not(h.has_item(h.has_entries(needle))))


def assert_response_valid(response):
    msg = "URL: %s, Response received: %s" % (response.url, unicode(response.data))
    h.assert_that(response.status, h.greater_than_or_equal_to(200), msg)
    h.assert_that(response.status, h.less_than(400), msg)


def not_empty():
    return h.is_not(h.has_length(0))
