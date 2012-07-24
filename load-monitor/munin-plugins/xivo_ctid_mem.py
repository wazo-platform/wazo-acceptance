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

class XivoCtidMem(MuninPlugin):
    args = '--base 1024 -l 0'
    title = 'XiVO CTID mem'
    vlabel = 'Bytes'
    scaled = False
    category = 'xivo'

    @property
    def fields(self):
        return [('cti_mem_res', dict(
                    label = 'cti_mem_res',
                    info = 'CTID resident memory consumption',
                    type = 'GAUGE',
                    draw = 'AREA',
                    min = '0')),
                ('cti_mem_virt', dict(
                    label = 'cti_mem_virt',
                    info = 'CTID virtual memory consumption',
                    type = 'GAUGE',
                    draw = 'LINE2',
                    min = '0'))]

    def execute(self):
        cti_pid = 0
        proc_name = '/usr/bin/xivo-ctid'
        for proc in psutil.process_iter():
            try:
                if proc.cmdline[1] == proc_name:
                    cti_pid = proc.pid
            except:
                continue

        if cti_pid == 0:
            print 'cti_mem_res.value 0'
            print 'cti_mem_virt.value 0'
            sys.exit(1)

        handler = psutil.Process(cti_pid)
        cti_mem_res, cti_mem_virt = handler.get_memory_info()

        print 'cti_mem_res.value %s' % str(cti_mem_res)
        print 'cti_mem_virt.value %s' % str(cti_mem_virt)
        

if __name__ == "__main__":
    XivoCtidMem().run()

