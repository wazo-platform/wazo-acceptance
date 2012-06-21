#!/usr/bin/python

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

        host = '192.168.32.126'
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

