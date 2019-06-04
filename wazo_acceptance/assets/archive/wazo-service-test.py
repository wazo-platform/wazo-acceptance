#!/usr/bin/env python
# Copyright 2016-2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import subprocess
import re

BASE_SERVICES = [
    'dahdi',
    'wazo-auth',
    'wazo-dird',
    'wazo-call-logd',
    'xivo-sysconfd',
    'xivo-confgend',
    'xivo-confd',
    'xivo-dxtora',
    'xivo-provd',
    'xivo-agid',
    'asterisk',
    'xivo-amid',
    'xivo-agentd',
    'xivo-ctid',
    'xivo-dird-phoned',
]

ALL_SERVICES = ['rabbitmq-server', 'consul', 'postgresql@9.6-main', 'nginx'] + BASE_SERVICES

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
    lines = _exec(['wazo-service'] + list(args))
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