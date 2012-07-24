#!/usr/bin/python

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


import sys, socket
from munin import MuninPlugin
"""
" http://github.com/samuel/python-munin
"""

class XivoCtidSocket(MuninPlugin):
    title = 'Xivo CTID socket'
    vlabel = 'Boolean'
    scaled = False
    category = 'xivo'

    @property
    def fields(self):
        return [('ctid_socket', dict(
                label = 'ctid_socket_status',
                info = 'Status of CTID socket',
                type = 'GAUGE',
                draw = 'AREA',
                min = '0',
                max = '1'))]

    def execute(self):

        host = '127.0.0.1'
        port = 5003

        # UDP port by changing "socket.SOCK_STREAM" to "socket.SOCK_DGRAM"
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            s.connect((host, port))
            s.shutdown(2)
            ctid_socket_status = 1
            """
            print "Success connecting to "
            print host + " on port: " + str(port)
            """
        except:
            ctid_socket_status = 0
            """
            print "Cannot connect to "
            print host + " on port: " + str(port)
            """

        print 'ctid_socket.value %s' % str(ctid_socket_status)

if __name__ == "__main__":
    XivoCtidSocket().run()

