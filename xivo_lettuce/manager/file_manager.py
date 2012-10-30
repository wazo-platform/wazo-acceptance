# -*- coding: UTF-8 -*-

import os
from lettuce.registry import world

SOUND_REC_PATH = '/usr/share/asterisk/sounds/recordings'
SOUND_REC_MEETME_PATH = '/var/lib/asterisk/sounds/meetme'
MOH_PATH = '/usr/share/asterisk/moh/default'


def create_recordings_file(filename):
    _touch_remote_file(os.path.join(SOUND_REC_PATH, filename))


def create_recordings_meetme_file(filename):
    _touch_remote_file(os.path.join(SOUND_REC_MEETME_PATH, filename))


def _touch_remote_file(abs_filename):
    world.ssh_client_xivo.check_call(['touch', abs_filename])


def create_musiconhold_file(filename):
    _touch_remote_file(os.path.join(MOH_PATH, filename))
