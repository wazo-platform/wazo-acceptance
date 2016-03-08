# -*- coding: utf-8 -*-

# Copyright (C) 2013-2016 Avencall
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

import os
import tempfile

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


def remove_remote_file(filename):
    world.ssh_client_xivo.call(['rm', '-f', filename])


def write_remote_file(filename, content, user=None):
    with tempfile.NamedTemporaryFile(delete=False) as f:
        local_filename = f.name
        f.write(content)
        f.close()
        world.ssh_client_xivo.send_files(local_filename, filename)
        if user:
            world.ssh_client_xivo.call(['chown', user, filename])

    return local_filename


def _touch_remote_file(abs_filename):
    world.ssh_client_xivo.check_call(['touch', abs_filename])
