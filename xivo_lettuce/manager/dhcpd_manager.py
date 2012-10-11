# -*- coding: utf-8 -*-

from lettuce import world
import time

MAX_RETRIES_TO_CONTACT_MONIT = 30
SECONDS_BETWEEN_RETRIES_TO_CONTACT_MONIT = 10


def type_pool_start_end(start, end):
    input_start = world.browser.find_element_by_id('it-pool_start', 'DHCP form not loaded')
    input_end = world.browser.find_element_by_id('it-pool_end')
    input_start.clear()
    input_start.send_keys(start)
    input_end.clear()
    input_end.send_keys(end)


def process_monitored(process_name):
    _wait_monit_restart(MAX_RETRIES_TO_CONTACT_MONIT)
    result = get_monit_status()
    for line in result:
        if line == "Process '%s'" % process_name:
            return True
    return False


def _wait_monit_restart(maxtries):
    nbtries = 0
    _ready = is_monit_started()
    while nbtries < maxtries and not _ready:
        time.sleep(SECONDS_BETWEEN_RETRIES_TO_CONTACT_MONIT)
        _ready = True if is_monit_started() else False
        nbtries += 1

    return _ready


def is_monit_started():
    result = get_monit_status()
    if 'monit: error connecting to the monit daemon' in result:
        return False
    return True


def get_monit_status():
    command = ['monit', 'status']
    result = world.ssh_client_xivo.out_err_call(command)
    return result.split('\n')
