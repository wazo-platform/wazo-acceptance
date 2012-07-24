#!/usr/bin/python
# -*- coding: UTF-8 -*-

# Copyright (C) 2012  Avencall
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


import sqlite3
from munin import MuninPlugin
"""
" http://github.com/samuel/python-munin
"""

class XivoDiskSpace(MuninPlugin):
    args = '--base 1024 -l 0'
    title = 'Average disk space by call'
    vlabel = 'Bytes'
    scaled = False
    category = 'xivo'

    @property

    def fields(self):
        return [('diskspacebycall', dict(
                label = 'Average disk space by call',
                info = 'Average space taken on disk for 1 call',
                type = 'GAUGE',
                draw = 'AREA',
                min = '0'))]

    def execute(self):
        db = '/tmp/diskspacebycall.db'
        table = 'tbl1'

        conn = sqlite3.connect(db)
        c = conn.cursor()

        c.execute('select * from %s' % table)
        results = c.fetchall()
        if len(results) < 2:
            average = 0
        else:
            first_disk_avail = results[0][3]
            last_disk_avail = results[-1][3]
            first_call = results[0][2]
            last_call = results[-1][2]
            average = (first_disk_avail - last_disk_avail) / (last_call - first_call)

        print 'diskspacebycall.value %s' % average

if __name__ == "__main__":
    XivoDiskSpace().run()
