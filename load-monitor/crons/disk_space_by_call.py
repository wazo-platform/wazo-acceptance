#!/usr/bin/python
# -*- coding: UTF-8 -*-

import argparse
import os
import sys
import telnetlib
import sqlite3


def main():
    parsed_args = _parse_args()

    mount_point = parsed_args.disk
    server = parsed_args.server
    db = parsed_args.db
    if mount_point == None:
        print '[Error] - partition disk not given'
        sys.exit(1)
    if server == None:
        print '[Error] - IP not given'
        sys.exit(1)
    if db == None:
        print '[Error] - DB not given'
        sys.exit(1)

    try:
        conn = sqlite3.connect(db)
    except:
        print '[Error] - No connection to DB'
        sys.exit(1)

    o = DiskSpaceByCall()
    o.process_data(conn, mount_point, server)

def _parse_args():
    parser = _new_argument_parser()
    return parser.parse_args()

def _new_argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--disk', type=str,
                        help='mount point that has to be monitored')
    parser.add_argument('-s', '--server', type=str,
                        help='IP of the asterisk server')
    parser.add_argument('-b', '--db', type=str,
                        help='SQLite Database, for munin plugins, please set db to /tmp/diskspacebycall.db')
    return parser

class TelnetAsterisk(object):
    def __init__(self):
        self.username = 'xivo_munin_user'
        self.password = 'jeSwupAd0'
        self.command = 'core show channels'

    def poll_asterisk(self, host):
        tn = self._init_socket(host)
        self._validate_connection(tn)
        data = self._get_data(tn, self.command)
        self._close_connection(tn)
        results = self._process_data(data)
        return results

    def _init_socket(self, host):
    
        timeout = 2
        port = 5038
        tn = telnetlib.Telnet()
    
        tn.open(host, port, timeout)
        tn.read_until("Asterisk Call Manager")
        tn.write("Action: login\r\n")
        tn.write("Username: %s\r\n" % self.username)
        tn.write("Secret: %s\r\n" % self.password)
        tn.write("Events: off\r\n")
        tn.write("\r\n")
        return tn
    
    def _validate_connection(self, tn):
        accepted = tn.read_until("Authentication accepted", 2)
        if not ( accepted.find('Authentication accepted') >= 0 ):
            print '[Error] : Asterisk authentication not accepted'
            sys.exit(1)
    
    def _get_data(self, tn, command):
        tn.write("Action: command\r\n")
        tn.write("Command: %s\r\n" % command)
        tn.write("\r\n")
        data = tn.read_until("calls processed")
        return data
    
    def _process_data(self, data):
        last_line = data.split('\n')[-1]
        results = last_line.split(' ')[0]
        return results
    
    def _close_connection(self, tn):
        tn.close()

class DiskSpaceByCall(object):
    def __init__(self):
        self.average = 0
        self.truncate = False

    def process_data(self, conn, mount_point, server):
        c = conn.cursor()
        # Calculate average, generate graphs and store data
        self.avail_disk = int(self._get_available_space(mount_point))
        # Asterisk process calls are for in and out, we only want in
        self.nb_calls = int(self._get_nb_calls(server)) / 2
        self._validate_table(c, 'tbl1')
        self.last_entry = self._get_last_entry(c)
        self._calculate_average()
        if self.truncate == True:
            _truncate_table(c, 'tbl1')
        # Finally, it's munin that generates graphs
        #_generate_graphs()
        self._store_data(c)
        conn.commit()
        c.close()
        #return self.average

    def _get_nb_calls(self, server):
        # Return numbers of calls processed by asterisk server
        t = TelnetAsterisk()
        return t.poll_asterisk(server)

    def _get_available_space(self, mount_point):
        # Return available disk space for the specified mount point
        s = os.statvfs(mount_point)
        return s.f_bsize * s.f_bavail

    def _get_last_entry(self, c):
        # Return last entry ( number of calls + available disk space ) from sqlite DB
        c.execute('SELECT * FROM tbl1 ORDER BY id DESC LIMIT 2')
        return c.fetchone()

    def _calculate_average(self):
        # Calculate average between disk consumption and number of calls
        if self.last_entry == None:
            calls = self.nb_calls
            disk_space = self.avail_disk
            # Can't calculate average if no past entries
            self.average = 0
        else:
            calls = self.nb_calls - self.last_entry[2]
            if calls < 0:
                calls = self.nb_calls
                # flush table if a new test is launched
                self.truncate = True
            disk_space = self.last_entry[3] - self.avail_disk
            self.average = disk_space / calls

    def _generate_graphs(self, avail_disk, nb_calls):
        # Generate graph disk_space/nb_calls and average/time
        print 'not implemented'

    def _store_data(self, c):
        # Store data in DB
        try:
            t = (self.nb_calls, self.avail_disk)
            c.execute('INSERT INTO tbl1 (nbCalls, diskSpace) VALUES (?,?)', t)
        except:
            print '[Error] - couldnt insert into database'
            raise
            sys.exit(1)

    def _truncate_table(self, c, table):
        c.execute('delete from %s' % table)

    def _validate_table(self, c, table):
        t = (table,)
        c.execute('select sql from sqlite_master where type = \'table\' and name = ?', t)
        if c.fetchone() == None:
            try:
                c.execute('CREATE TABLE %s ( id INTEGER PRIMARY KEY AUTOINCREMENT, t TIMESTAMP DEFAULT CURRENT_TIMESTAMP, nbCalls INTEGER, diskSpace INTEGER)' % table)
                """
                sqlite3 table schema : 
                sqlite> create table tbl1 (
                ...> id INTEGER PRIMARY KEY AUTOINCREMENT,
                ...> t TIMESTAMP
                ...> DEFAULT CURRENT_TIMESTAMP,
                ...> nbCalls INTEGER,
                ...> diskSpace INTEGER
                ...> );
                """
            except:
                print '[Error] - couldn\'t create table in database'
                sys.exit(1)

if __name__ == "__main__":
    main()
