# -*- coding: utf-8 -*-

# Copyright (C) 2013 Avencall
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

from xivo_lettuce import postgres
from xivo_dao.data_handler.call_log import dao
from xivo_dao.data_handler.call_log.model import CallLog


def delete_all():
    dao.delete_all()


def delete_entries_between(start, end):
    query = "DELETE FROM call_log WHERE date BETWEEN :start AND :end"
    postgres.execute_sql(query, start=start, end=end)


def _format_condition(key, value):
    if value == 'NULL':
        return '%s IS NULL' % key
    else:
        return '%s = :%s' % (key, key)


def has_call_log(entry):
    base_query = """SELECT COUNT(*) FROM call_log"""
    conditions = ' AND '.join(_format_condition(k, v) for k, v in entry.iteritems())
    if conditions:
        query = '%s WHERE %s' % (base_query, conditions)
    else:
        query = base_query

    count = postgres.execute_sql(query, **entry).scalar()
    return count > 0


def create_call_logs(entries):
    call_logs = [CallLog(**entry) for entry in entries]
    dao.create_all(call_logs)
