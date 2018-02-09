# -*- coding: utf-8 -*-
# Copyright (C) 2013-2016 Avencall
# Copyright (C) 2016 Proformatique Inc.
# SPDX-License-Identifier: GPL-3.0+

import os

from lettuce import world

BACKUP_PATH = '/var/backups/xivo'
MOH_PATH = '/usr/share/asterisk/moh/default'
SOUND_REC_PATH = '/usr/share/asterisk/sounds/recordings'
SOUND_REC_MEETME_PATH = '/var/lib/asterisk/sounds/meetme'


def create_backup_file(filename):
    _touch_remote_file(os.path.join(BACKUP_PATH, filename))


def create_musiconhold_file(filename):
    _touch_remote_file(os.path.join(MOH_PATH, filename))


def create_recordings_file(filename):
    _touch_remote_file(os.path.join(SOUND_REC_PATH, filename))


def create_recordings_meetme_file(filename):
    _touch_remote_file(os.path.join(SOUND_REC_MEETME_PATH, filename))


def create_empty_file(path):
    # if the file already exist on the fs, it will be truncated to 0
    world.ssh_client_xivo.check_call(['truncate', '-s0', path])


def _touch_remote_file(abs_filename):
    world.ssh_client_xivo.check_call(['touch', abs_filename])
