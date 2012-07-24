#!/usr/bin/env python 

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

import sys, psutil
from munin import MuninPlugin
"""
" http://github.com/samuel/python-munin
"""

class PgsqlMem(MuninPlugin):
    args = '--base 1024 -l 0'
    title = 'Pgsql mem'
    vlabel = 'Bytes'
    scaled = False
    category = 'postgresql'

    @property
    def fields(self):
        return [('pg_mem_res', dict(
                    label = 'pg_mem_res',
                    info = 'Postgresql resident memory consumption',
                    type = 'GAUGE',
                    draw = 'AREA',
                    min = '0')),
                ('pg_mem_virt', dict(
                    label = 'pg_mem_virt',
                    info = 'Postgresql virtual memory consumption',
                    type = 'GAUGE',
                    draw = 'LINE2',
                    min = '0'))]

    def execute(self):
        pg_pid = []
        proc_name = 'postgres'
        for proc in psutil.process_iter():
            if proc.name.find(proc_name) >= 0 :
                pg_pid.append(proc.pid)

        if len(pg_pid) <  1:
            print 'pg_mem_res.value 0'
            print 'pg_mem_virt.value 0'
            sys.exit(1)

        pg_mem_res = 0
        pg_mem_virt = 0
        for pid in pg_pid:
            handler = psutil.Process(pid)
            pg_mem_res += handler.get_memory_info()[0]
            pg_mem_virt += handler.get_memory_info()[1]

#        print 'pg_mem_res.value %s' % str(pg_mem_res/1024/1024)
#        print 'pg_mem_virt.value %s' % str(pg_mem_virt/1024/1024)
        print 'pg_mem_res.value %s' % str(pg_mem_res)
        print 'pg_mem_virt.value %s' % str(pg_mem_virt)
        

if __name__ == "__main__":
    PgsqlMem().run()

