# -*- coding: utf-8 -*-
# Copyright 2013-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from xivo_acceptance.lettuce import postgres


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
