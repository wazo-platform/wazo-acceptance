# -*- coding: UTF-8 -*-

import time
from lettuce.registry import world


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


def send_command(command):
    res = world.ssh_client_xivo.check_call(command) == 0
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
    if service == 'asterisk':
        return '/var/run/asterisk/asterisk.pid'
    elif service == 'xivo-ctid':
        return '/var/run/xivo-ctid.pid'
    else:
        assert False, 'Service %s must be implemented' % service
