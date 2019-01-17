# -*- coding: utf-8 -*-
# Copyright (C) 2013-2014 Avencall
# SPDX-License-Identifier: GPL-3.0-or-later

from xivo_acceptance.lettuce import postgres


def delete(dialpattern_id):
    query = """
    DELETE FROM
        dialpattern
    WHERE
        dialpattern.id = :dialpattern_id
    """
    postgres.exec_sql_request(query, dialpattern_id=dialpattern_id)
