#!/usr/bin/env python3
# Copyright 2016-2025 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import re
import subprocess
import time

BASE_SERVICES = [
    'asterisk',
    'wazo-agentd',
    'wazo-agid',
    'wazo-amid',
    'wazo-auth',
    'wazo-call-logd',
    'wazo-calld',
    'wazo-chatd',
    'wazo-confd',
    'wazo-confgend',
    'wazo-dird',
    'wazo-dxtora',
    'wazo-phoned',
    'wazo-plugind',
    'wazo-provd',
    'wazo-webhookd',
    'wazo-websocketd',
    'wazo-sysconfd',
]

ALL_SERVICES = ['rabbitmq-server', 'postgresql@15-main', 'nginx'] + BASE_SERVICES

MONIT_RUNNING = re.compile(r'^\d+ monit$')
RUNNING_SERVICE = re.compile(r'^\s+(?:running|unknown)\s+(\S+)$')
STOPPED_SERVICE = re.compile(r'^\s+(?:stopped|unknown)\s+(\S+)$')
STARTING_SERVICE = re.compile(r'^\s+starting (\S+) ... (?:OK|ignored)$')


def _exec(cmd):
    print(' '.join(cmd))
    lines = subprocess.run(cmd, capture_output=True, encoding='utf-8').stdout
    lines = lines.split('\n')
    for line in lines:
        print(line)
    return lines


def _retry(timeout: float, interval: float):
    start_time = time.monotonic()
    while time.monotonic() < (start_time + timeout):
        yield
        time.sleep(interval)


def _monit_is_running():
    for _ in _retry(timeout=5, interval=1):
        lines = _exec(['pgrep', '-l', 'monit'])
        is_running = any(MONIT_RUNNING.match(line) for line in lines)
        if is_running:
            return True
    return False


def _monit_is_not_running():
    for _ in _retry(timeout=5, interval=1):
        lines = _exec(['pgrep', '-l', 'monit'])
        is_running = any(MONIT_RUNNING.match(line) for line in lines)
        if not is_running:
            return True
    else:
        return False


def _wazo_service(*args):
    lines = _exec(['wazo-service'] + list(args))
    return lines


def _are_services_running(services):
    return _are_services_matching(RUNNING_SERVICE, services)


def _are_services_stopped(services):
    return _are_services_matching(STOPPED_SERVICE, services)


def _are_services_matching(matcher, services):
    output = _wazo_service('status')
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
        print('Unmatched items', to_match)
        return False
    else:
        return True


def main():
    assert _monit_is_running()
    assert _are_services_running(BASE_SERVICES)

    _wazo_service('stop')
    assert _monit_is_not_running()
    assert _are_services_stopped(BASE_SERVICES)

    output = _wazo_service('start')
    assert _are_services_starting(output, BASE_SERVICES)
    assert _are_services_running(BASE_SERVICES)
    assert _monit_is_running()

    output = _wazo_service('restart', 'all')
    assert _are_services_starting(output, ALL_SERVICES)
    assert _monit_is_running()


if __name__ == '__main__':
    main()
