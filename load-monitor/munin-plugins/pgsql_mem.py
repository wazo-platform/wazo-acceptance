#!/usr/bin/env python 

import sys, psutil
from munin import MuninPlugin
"""
" http://github.com/samuel/python-munin
"""

class PgsqlMem(MuninPlugin):
    title = 'Pgsql mem'
    vlabel = 'MBytes'
    scaled = False
    category = 'postgresql'

    @property
    def fields(self):
        return [('pgsql_mem_res', dict(
                    label = 'pgsql_mem_res',
                    info = 'Postgresql resident memory consumption',
                    type = 'GAUGE',
                    draw = 'AREA',
                    min = '0')),
                ('pgsql_mem_virt', dict(
                    label = 'pgsql_mem_virt',
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

        print 'pg_mem_res.value %s' % str(pg_mem_res/1024/1024)
        print 'pg_mem_virt.value %s' % str(pg_mem_virt/1024/1024)
        

if __name__ == "__main__":
    PgsqlMem().run()

