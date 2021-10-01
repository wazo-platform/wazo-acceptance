# Copyright 2019-2021 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later


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
