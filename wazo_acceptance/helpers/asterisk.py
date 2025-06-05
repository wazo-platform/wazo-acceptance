# Copyright 2019-2023 The Wazo Authors  (see the AUTHORS file)
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
        return ['asterisk', '-rx', f'"{asterisk_command}"']

    def _find_channel(self, peer_name):
        channels = self.send_to_asterisk_cli('core show channels')
        for channel in channels.splitlines:
            if channel.startswith('PJSIP/' + peer_name):
                return channel
        return None

    def get_current_call_codec(self, peer_name):
        channel = self._find_channel(peer_name)
        details = self.send_to_asterisk_cli('core show channel ' + channel)
        for line in details.splitlines:
            # example: '     NativeFormats: (opus)'
            if line.lstrip().startswith('NativeFormats:'):
                return line.split(': ')[1][1:-1]
