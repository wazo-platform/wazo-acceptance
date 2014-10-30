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

from xivo_acceptance.lettuce import postgres


def delete_all():
    query = "DELETE FROM cel"
    postgres.exec_sql_request(query)


def delete_entries_between(start, end):
    query = "DELETE FROM cel WHERE eventtime BETWEEN :start AND :end"
    postgres.exec_sql_request(query, start=start, end=end)


def insert_entries(entries):
    for entry in entries:
        cel = dict(entry)

        for key in ['userdeftype', 'cid_ani', 'cid_rdnis', 'cid_dnid', 'channame', 'appname', 'appdata', 'accountcode', 'peeraccount', 'peer']:
            cel.setdefault(key, '')

        cel.setdefault('amaflags', 0)
        if 'call_log_id' in cel and cel['call_log_id']:
            cel['call_log_id'] = int(cel['call_log_id'])
        else:
            cel['call_log_id'] = None

        query = """INSERT INTO cel VALUES (
                      DEFAULT,
                      :eventtype,
                      :eventtime,
                      :userdeftype,
                      :cid_name,
                      :cid_num,
                      :cid_ani,
                      :cid_rdnis,
                      :cid_dnid,
                      :exten,
                      :context,
                      :channame,
                      :appname,
                      :appdata,
                      :amaflags,
                      :accountcode,
                      :peeraccount,
                      :uniqueid,
                      :linkedid,
                      :userfield,
                      :peer,
                      :call_log_id
                      )"""

        postgres.exec_sql_request(query, **cel)
