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

import sys, telnetlib
from munin import MuninPlugin
"""
" http://github.com/samuel/python-munin
"""

def init_socket(host, username, password):

    timeout = 2
    port = 5038
    tn = telnetlib.Telnet()

    tn.open(host, port, timeout)
    tn.read_until("Asterisk Call Manager")
    tn.write("Action: login\r\n")
    tn.write("Username: %s\r\n" % username)
    tn.write("Secret: %s\r\n" % password)
    tn.write("Events: off\r\n")
    tn.write("\r\n")
    return tn

def validate_connection(tn):
    accepted = tn.read_until("Authentication accepted", 2)
    if not ( accepted.find('Authentication accepted') >= 0 ):
        print 'ERROR : Authentication not accepted'
        sys.exit(1)

def get_data(tn, command):
    tn.write("Action: command\r\n")
    tn.write("Command: %s\r\n" % command)
    tn.write("\r\n")
    data = tn.read_until("calls processed")
    return data

def process_data(data):
    last_line = data.split('\n')[-1]
    results = last_line.split(' ')[0]
    return results

def close_connection(tn):
    tn.close()

def print_output(results):
    print 'asteriskcalls.value %s' % results

class XivoCtidSocket(MuninPlugin):
    title = 'Asterisk calls processed'
    vlabel = 'Nb of Calls'
    scaled = False
    category = 'xivo'

    @property

    def fields(self):
        return [('asteriskcalls', dict(
                label = 'Calls processed since last restart',
                info = 'Number of calls processed by asterisk since last restart',
                type = 'GAUGE',
                draw = 'AREA',
                min = '0'))]

    def execute(self):
        host = '127.0.0.1'
        username = 'xivo_munin_user'
        password = 'jeSwupAd0'
        command = 'core show channels'

        tn = init_socket(host, username, password)
        validate_connection(tn)
        data = get_data(tn, command)
        close_connection(tn)
        results = process_data(data)
        print_output(results)

if __name__ == "__main__":
    XivoCtidSocket().run()

