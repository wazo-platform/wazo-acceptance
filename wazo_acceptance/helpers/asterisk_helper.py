# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later


def send_to_asterisk_cli(context, asterisk_command):
    context.ssh_client.call(_format_command(asterisk_command))


def _format_command(asterisk_command):
    return ['asterisk', '-rx', '"{}"'.format(asterisk_command)]
