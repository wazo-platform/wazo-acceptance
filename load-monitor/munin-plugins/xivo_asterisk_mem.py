#!/usr/bin/env python 

import sys, psutil
from munin import MuninPlugin
"""
" http://github.com/samuel/python-munin
"""

class XivoAsteriskMem(MuninPlugin):
    args = '--base 1024 -l 0'
    title = 'XiVO Asterisk mem'
    vlabel = 'Bytes'
    scaled = False
    category = 'xivo'

    @property
    def fields(self):
        return [('ast_mem_res', dict(
                    label = 'ast_mem_res',
                    info = 'Asterisk resident memory consumption',
                    type = 'GAUGE',
                    draw = 'AREA',
                    min = '0')),
                ('ast_mem_virt', dict(
                    label = 'ast_mem_virt',
                    info = 'Asterisk virtual memory consumption',
                    type = 'GAUGE',
                    draw = 'LINE2',
                    min = '0'))]

    def execute(self):
        ast_pid = 0
        proc_name = '/usr/sbin/asterisk'
        for proc in psutil.process_iter():
            try:
                if proc.cmdline[0] == proc_name:
                    ast_pid = proc.pid
            except:
                continue

        if ast_pid == 0:
            print 'ast_mem_res.value 0'
            print 'ast_mem_virt.value 0'
            sys.exit(1)

        handler = psutil.Process(ast_pid)
        ast_mem_res, ast_mem_virt = handler.get_memory_info()

        print 'ast_mem_res.value %s' % str(ast_mem_res)
        print 'ast_mem_virt.value %s' % str(ast_mem_virt)
        

if __name__ == "__main__":
    XivoAsteriskMem().run()

