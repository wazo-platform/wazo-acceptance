# Copyright 2019-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import time
import logging

logger = logging.getLogger('acceptance')


class Asterisk:

    def __init__(self, ssh_client):
        self._ssh_client = ssh_client

    def send_to_asterisk_cli(self, asterisk_command):
        response = self._ssh_client.out_call(self._format_command(asterisk_command))
        if asterisk_command.startswith('test ') and response.startswith("No such command 'test"):
            raise Exception('chan_test.so needs to be loaded on the stack')
        return response

    def _format_command(self, asterisk_command):
        return ['asterisk', '-rx', '"{}"'.format(asterisk_command)]

    def wait_until_reload_completed(self, retry=10, delay=1):
        # NOTE(fblackburn): Flaky method to know if reload is always in progress. But it should be
        # enough to resync reload when tests are running on slow host
        command = ['pgrep', 'wazo-confgen']
        for n in range(retry):
            reload_in_progress = not bool(self._ssh_client.call(command))
            if not reload_in_progress:
                # Ensure 2 consecutive false result
                time.sleep(1)
                reload_in_progress = not bool(self._ssh_client.call(command))
                if not reload_in_progress:
                    return
            time.sleep(delay)

        logger.warning('wazo-confgen is still in progress after %s seconds', retry * delay)
