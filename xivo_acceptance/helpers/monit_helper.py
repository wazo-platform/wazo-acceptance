# -*- coding: utf-8 -*-
# Copyright 2013-2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import time

from lettuce import world

MAX_RETRIES_TO_CONTACT_MONIT = 30
SECONDS_BETWEEN_RETRIES_TO_CONTACT_MONIT = 10


def process_monitored(process_name):
    _wait_monit_restart(MAX_RETRIES_TO_CONTACT_MONIT)
    result = get_monit_status()
    for line in result:
        if line == "Process '%s'" % process_name:
            return True
    return False


def _wait_monit_restart(maxtries):
    for _ in xrange(maxtries):
        ready = is_monit_started()
        if ready:
            break
        time.sleep(SECONDS_BETWEEN_RETRIES_TO_CONTACT_MONIT)
    return ready


def is_monit_started():
    result = get_monit_status()
    if 'Cannot create socket to [localhost]:2812 -- Connection refused' in result:
        return False
    return True


def get_monit_status():
    command = ['monit', 'status']
    result = world.ssh_client_xivo.out_err_call(command)
    return result.split('\n')
