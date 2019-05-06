# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later


class AsteriskHelper:

    def __init__(self, ssh_client):
        self._ssh_client = ssh_client

    def send_to_asterisk_cli(self, asterisk_command):
        self._ssh_client.call(self._format_command(asterisk_command))

    def _format_command(self, asterisk_command):
        return ['asterisk', '-rx', '"{}"'.format(asterisk_command)]
