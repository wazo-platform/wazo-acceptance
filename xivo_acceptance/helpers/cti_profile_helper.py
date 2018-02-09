# -*- coding: utf-8 -*-
# Copyright (C) 2013-2014 Avencall
# Copyright (C) 2016 Proformatique Inc.
# SPDX-License-Identifier: GPL-3.0+

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
