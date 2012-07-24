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

class XivoClientMem(MuninPlugin):
    title = 'Xivoclient mem'
    vlabel = 'MBytes'
    scaled = False
    category = 'xivo'

    @property
    def fields(self):
        return [('xc_mem_res', dict(
                label = 'xc_mem_res',
                info = 'Xivo client resident memory consumption',
                type = 'GAUGE',
                draw = 'AREA',
                min = '0')),
                ('xc_mem_virt', dict(
                label = 'xc_mem_virt',
                info = 'Xivo client virtual memory consumption',
                type = 'GAUGE',
                draw = 'LINE2',
                min = '0'))]

    def execute(self):
        xc_pid = []
        proc_name = 'xivoclient'
        for proc in psutil.process_iter():
            if proc.name == proc_name:
                xc_pid.append(proc.pid)

        if len(xc_pid) <  1:
            print 'xc_mem_res.value 0'
            print 'xc_mem_virt.value 0'
            exit()

        handler = psutil.Process(xc_pid[0])
        xc_mem_res, xc_mem_virt = handler.get_memory_info()

        print 'xc_mem_res.value %s' % str(xc_mem_res/1024/1024)
        print 'xc_mem_virt.value %s' % str(xc_mem_virt/1024/1024)

if __name__ == "__main__":
    XivoClientMem().run()

