import psutil, sys

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


def print_mem(n, name, title):

    arguments = sys.argv

    import os, msvcrt
    msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)

    if len(arguments) > 1:
        if arguments[1] == 'config':
            print 'graph_order xc_mem_rss xc_mem_vms'
            print 'graph_title ' + title
            print 'graph_args --vertical-label MBytes'
            print 'graph_category xivo'
            print 'graph_info This graph the memory consumption of xivoclient'
            print 'xc_mem_rss.label Xivoclient Resident memory'
            print 'xc_mem_rss.draw AREA'
            print 'xc_mem_vms.label Xivoclient Virtual memory'
            print 'xc_mem_vms.draw LINE2'
            print '.'
            exit()
        elif arguments[1] == 'name':
            print name
            exit()

    xc_pid = []
    proc_name = 'xivoclient.exe'
    for proc in psutil.process_iter():
        if proc.name == proc_name:
            xc_pid.append(proc.pid)

    if len(xc_pid) < n + 1:
        print 'xc_mem_rss.value 0'
        print 'xc_mem_vms.value 0'
        print '.'
        exit()

    handler = psutil.Process(xc_pid[n])
    xc_mem_stats = handler.get_memory_info()
    xc_mem_rss = xc_mem_stats.rss
    xc_mem_vms = xc_mem_stats.vms

    print 'xc_mem_rss.value ' + str(xc_mem_rss/1024/1024)
    print 'xc_mem_vms.value ' + str(xc_mem_vms/1024/1024)
    print '.'

