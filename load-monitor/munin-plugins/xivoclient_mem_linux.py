#!/usr/bin/env python 

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
        proc_cmdline = './xivoclient'
        for proc in psutil.process_iter():
            if proc.name == proc_name:
                if proc.cmdline[0] == proc_cmdline:
                    xc_pid.append(proc.pid)

        if len(xc_pid) <  1:
            print 'xc_mem_res.value 0'
            print 'xc_mem_virt.value 0'
            exit()

        handler = psutil.Process(xc_pid[0])
        if sys.platform == 'win32':
            xc_mem_stats = handler.get_memory_info()
            xc_mem_res = xc_mem_stats.res
            xc_mem_virt = xc_mem_stats.virt
        else:
            xc_mem_res, xc_mem_virt = handler.get_memory_info()

        print 'xc_mem_res.value %s' % str(xc_mem_res/1024/1024)
        print 'xc_mem_virt.value %s' % str(xc_mem_virt/1024/1024)

if __name__ == "__main__":
    XivoClientMem().run()

