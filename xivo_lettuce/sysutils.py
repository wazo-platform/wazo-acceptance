# -*- coding: utf-8 -*-

# Copyright (C) 2013 Avencall
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

import time
from lettuce import world


SERVICE_PIDFILES = {
    'asterisk': '/var/run/asterisk/asterisk.pid',
    'xivo-ctid': '/var/run/xivo-ctid.pid',
    'xivo-agent': '/var/run/xivo-agentd.pid',
}


def path_exists(path):
    command = ['ls', path]
    try:
        return world.ssh_client_xivo.check_call(command) == 0
    except Exception:
        return False


def dir_is_empty(path):
    command = ['ls', '-1A', path, '|', 'wc', '-l']
    return world.ssh_client_xivo.out_call(command).strip() == '0'


def get_list_file(path):
    command = ['ls', path]
    return world.ssh_client_xivo.out_call(command)


def file_owned_by_user(path, owner):
    command = ['stat', '-c', '%U', path]
    return world.ssh_client_xivo.out_call(command).strip() == owner


def file_owned_by_group(path, owner):
    command = ['stat', '-c', '%G', path]
    return world.ssh_client_xivo.out_call(command).strip() == owner


def get_content_file(path):
    command = ['cat', path]
    return world.ssh_client_xivo.out_call(command)


def send_command(command, check=True):
    if check:
        res = world.ssh_client_xivo.check_call(command) == 0
    else:
        res = world.ssh_client_xivo.call(command) == 0
    time.sleep(1)
    return res


def output_command(command):
    res = world.ssh_client_xivo.out_call(command)
    time.sleep(1)
    return res


def is_process_running(pidfile):
    if not path_exists(pidfile):
        return False
    pid = get_content_file(pidfile).strip()
    return path_exists("/proc/%s" % pid)


def wait_service_restart(pidfile, maxtries=15, wait_secs=10):
    nbtries = 0
    restarted = is_process_running(pidfile)
    while nbtries < maxtries and not restarted:
        time.sleep(wait_secs)
        restarted = is_process_running(pidfile)
        nbtries += 1

    return restarted


def get_pidfile_for_service_name(service):
    pidfile = SERVICE_PIDFILES.get(service, None)
    if not pidfile:
        assert False, 'Service %s must be implemented' % service
    return pidfile
