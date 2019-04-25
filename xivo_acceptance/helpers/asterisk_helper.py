# -*- coding: utf-8 -*-
# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from lettuce import world


def send_to_asterisk_cli(asterisk_command):
    world.ssh_client_xivo.call(_format_command(asterisk_command))


def _format_command(asterisk_command):
    return [u'asterisk', u'-rx', u'"{}"'.format(asterisk_command)]
