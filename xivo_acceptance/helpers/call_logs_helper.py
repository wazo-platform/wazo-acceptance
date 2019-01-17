# -*- coding: utf-8 -*-
# Copyright 2013-2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from xivo_acceptance.lettuce import postgres
from xivo_dao.resources.call_log import dao
from xivo_dao.alchemy.call_log import CallLog
from xivo_dao.helpers.db_utils import session_scope


def delete_all():
    query = 'DELETE FROM call_log'
    postgres.exec_sql_request(query)


def _format_condition(key, value):
    if value == 'NULL':
        return '%s IS NULL' % key
    else:
        return '%s = :%s' % (key, key)


def has_call_log(entry):
    query = _query_from_entry(entry)

    return postgres.exec_sql_request(query, **entry).scalar()


def find_last_call_log():
    query = '''SELECT date,
                      date_answer,
                      date_end,
                      source_name,
                      source_exten,
                      destination_name,
                      destination_exten,
                      user_field,
               FROM call_log
               ORDER BY date DESC
               LIMIT 1'''

    call_log = postgres.exec_sql_request(query).fetchone()

    return {'date': call_log[0],
            'date_answer': call_log[1],
            'date_end': call_log[2],
            'source_name': call_log[3],
            'source_exten': call_log[4],
            'destination_name': call_log[5],
            'destination_exten': call_log[6],
            'user_field': call_log[8]} if call_log else None


def _query_from_entry(entry):
    base_query = """SELECT count(*) FROM call_log"""
    conditions = ' AND '.join(_format_condition(k, v) for k, v in entry.iteritems())
    query = '%s WHERE %s' % (base_query, conditions)
    return query


def create_call_logs(entries):
    call_logs = [CallLog(**entry) for entry in entries]
    with session_scope():
        dao.create_from_list(call_logs)
