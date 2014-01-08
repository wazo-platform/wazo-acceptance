# -*- coding: utf-8 -*-

# Copyright (C) 2013-2014 Avencall
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
    if 'monit: error connecting to the monit daemon' in result:
        return False
    return True


def get_monit_status():
    command = ['monit', 'status']
    result = world.ssh_client_xivo.out_err_call(command)
    return result.split('\n')
