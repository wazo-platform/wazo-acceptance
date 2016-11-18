# -*- coding: utf-8 -*-

# Copyright (C) 2013-2014 Avencall
# Copyright (C) 2016 Proformatique Inc.
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

from xivo_acceptance.lettuce import postgres
from hamcrest import assert_that, is_not, none


def get_id_with_name(profile_name):
    profile_id = find_profile_id_by_name(profile_name)
    assert_that(profile_id, is_not(none()),
                "CTI profile '%s' not found" % profile_name)
    return profile_id


def find_profile_id_by_name(profile_name):
    query = """
    SELECT
        id
    FROM
        cti_profile
    WHERE
        name = :profile_name
    """

    result = postgres.exec_sql_request(query,
                                       profile_name=profile_name)
    return result.scalar()
