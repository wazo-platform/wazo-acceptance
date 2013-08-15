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


from xivo_lettuce import form, postgres


def type_date(date):
    form.input.set_text_field_with_id('it-dbeg', date)


def delete_all():
    query = "DELETE FROM call_log"
    postgres.execute_sql(query)


def delete_entries_between(start, end):
    query = "DELETE FROM call_log WHERE date BETWEEN :start AND :end"
    postgres.execute_sql(query, start=start, end=end)


def has_call_log(entry):
    query = """SELECT COUNT(*) FROM call_log WHERE
        date = :date AND
        destination_name = :destination_name AND
        destination_exten = :destination_exten AND
        source_name = :source_name AND
        source_exten = :source_exten AND
        duration = :duration AND
        user_field = :user_field AND
        answered = :answered"""

    res = postgres.execute_sql(query, **entry)
    if res is not None and len(res.fetchall()) == 1:
        return True
    else:
        return False
