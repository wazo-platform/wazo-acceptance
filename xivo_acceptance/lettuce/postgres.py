# -*- coding: utf-8 -*-
# Copyright (C) 2013-2014 Avencall
# SPDX-License-Identifier: GPL-3.0+

from sqlalchemy.sql import text
from xivo_dao.helpers.db_utils import session_scope


def exec_sql_request(query, **args):
    with session_scope() as session:
        return session.execute(text(query), args)


def exec_count_request(table, **cond_dict):
    pg_command = 'SELECT COUNT(*) FROM "%s"' % table
    if len(cond_dict) > 0:
        pg_command += " WHERE "
        cond = []
        for key, value in cond_dict.iteritems():
            cond.append('%s = %s' % (key, value))
        pg_command = '%s%s' % (pg_command, ' AND '.join(cond))

    with session_scope() as session:
        result = session.execute(pg_command)
        row = result.fetchone()
        return int(row[0])
