# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from xivo_test_helpers import until


class Monit:

    def __init__(self, context):
        self._ssh_client = context.ssh_client

    def process_monitored(self, process_name):
        until.true(self.is_monit_started, timeout=60, interval=10, message='Monit is unreachable')
        result = self.get_monit_status()
        for line in result:
            if line == "Process '%s'" % process_name:
                return True
        return False

    def is_monit_started(self):
        result = self.get_monit_status()
        if 'Cannot create socket to [localhost]:2812 -- Connection refused' in result:
            return False
        return True

    def get_monit_status(self):
        command = ['monit', 'status']
        result = self._ssh_client.out_err_call(command)
        return result.split('\n')
