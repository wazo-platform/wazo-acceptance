# -*- coding: utf-8 -*-
# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later


def send_to_asterisk_cli(context, asterisk_command):
    context.ssh_client_xivo.call(_format_command(asterisk_command))


def _format_command(asterisk_command):
    return [u'asterisk', u'-rx', u'"{}"'.format(asterisk_command)]
