#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2016 Avencall
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

import subprocess
import re

BASE_SERVICES = [
    'dahdi',
    'xivo-sysconfd',
    'xivo-confgend',
    'xivo-confd',
    'xivo-auth',
    'xivo-dxtora',
    'xivo-provd',
    'xivo-agid',
    'asterisk',
    'xivo-amid',
    'xivo-call-logs',
    'xivo-agentd',
    'xivo-ctid',
    'xivo-dird',
    'xivo-dird-phoned',
]

ALL_SERVICES = ['rabbitmq-server', 'consul', 'postgresql@9.4-main', 'nginx'] + BASE_SERVICES

MONIT_RUNNING = re.compile(r'^\d+ monit$')
RUNNING_SERVICE = re.compile(r'^\s+running\s+(\S+)$')
STOPPED_SERVICE = re.compile(r'^\s+stopped\s+(\S+)$')
STARTING_SERVICE = re.compile(r'^\s+starting (\S+) ... OK$')


def _exec(cmd):
    print ' '.join(cmd)
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    lines, _ = p.communicate()
    lines = lines.split('\n')
    for line in lines:
        print line
    return lines


def _is_monit_running():
    lines = _exec(['pgrep', '-l', 'monit'])
    matched = False
    for line in lines:
        if MONIT_RUNNING.match(line) is not None:
            matched = True
    return matched


def _xivo_service(*args):
    lines = _exec(['xivo-service'] + list(args))
    return lines


def _are_services_running(services):
    return _are_services_matching(RUNNING_SERVICE, services)


def _are_services_stopped(services):
    return _are_services_matching(STOPPED_SERVICE, services)


def _are_services_matching(matcher, services):
    output = _xivo_service('status')
    return _are_all_items_matched_in_buffer(output, matcher, services)


def _are_services_starting(output, services):
    return _are_all_items_matched_in_buffer(output, STARTING_SERVICE, services)


def _are_all_items_matched_in_buffer(buf, matcher, items):
    to_match = set(items)
    for line in buf:
        match = matcher.match(line)
        if match is None:
            continue
        to_match.discard(match.group(1))

    if to_match:
        print 'Unmatched items', to_match
        return False
    else:
        return True


def main():
    assert _is_monit_running()
    assert _are_services_running(BASE_SERVICES)

    _xivo_service('stop')
    assert not _is_monit_running()
    assert _are_services_stopped(BASE_SERVICES)

    output = _xivo_service('start')
    assert _are_services_starting(output, BASE_SERVICES)
    assert _is_monit_running()
    assert _are_services_running(BASE_SERVICES)

    output = _xivo_service('restart', 'all')
    assert _are_services_starting(output, ALL_SERVICES)
    assert _is_monit_running()


if __name__ == '__main__':
    main()
