# -*- coding: utf-8 -*-

# Copyright (C) 2013-2014 Avencall
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

import re

from hamcrest import *
from lettuce import step

from xivo_acceptance.helpers import file_helper
from xivo_lettuce import sysutils


ASTERISK_VM_PATH = '/var/spool/asterisk/voicemail'
BACKUP_DIR = '/var/backups/xivo'
MOH_PATH = '/usr/share/asterisk/moh/default'
DAHDI_PATH = '/dev/dahdi'
ASTERISK_SOUND_PATH = '/usr/share/asterisk/sounds/en'


@step(u'Given a backup file with name "([^"]*)"')
def given_a_backup_file_with_name(step, filename):
    file_helper.create_backup_file(filename)


@step(u'Given a musiconhold file with name "([^"]*)"')
def given_a_musiconhold_file_with_name(step, filename):
    file_helper.create_musiconhold_file(filename)


@step(u'Given a recording file with name "([^"]*)"')
def given_a_recording_file_with_name(step, filename):
    file_helper.create_recordings_file(filename)


@step(u'Given a recording meetme file with name "([^"]*)"')
def given_a_recording_meetme_file_with_name(step, filename):
    file_helper.create_recordings_meetme_file(filename)


@step(u'Then directory of the Asterisk voicemail is empty')
def then_directory_of_the_asterisk_voicemail_is_empty(step):
    assert sysutils.dir_is_empty(ASTERISK_VM_PATH)


@step(u'Then Asterisk sound files correctly installed')
def then_asterisk_sound_files_correctly_installed(step):
    assert not sysutils.dir_is_empty(ASTERISK_SOUND_PATH)


@step(u'Then Asterisk owns /dev/dadhi')
def then_asterisk_owns_dev_dadhi(step):
    text = sysutils.get_list_file(DAHDI_PATH)
    lines = text.split("\n")
    for line in lines:
        if line:
            file = '%s/%s' % (DAHDI_PATH, line.strip())
            assert sysutils.file_owned_by_user(file, 'asterisk')


@step(u'Then MOH files owned by asterisk:www-data')
def then_moh_files_owned_by_asterisk_www_data(step):
    command = ['apt-get', 'install', '-y', 'asterisk-moh-opsound-wav']
    sysutils.send_command(command)
    text = sysutils.get_list_file(MOH_PATH)
    lines = text.split("\n")
    for line in lines:
        if line:
            file = '%s/%s' % (MOH_PATH, line.strip())
            assert sysutils.file_owned_by_user(file, 'asterisk')
            assert sysutils.file_owned_by_group(file, 'www-data')


@step(u'Then backup files successfully rotated')
def then_backup_files_successfully_rotated(step):
    command = ['rm', '-f', '%s/*' % BACKUP_DIR]
    sysutils.send_command(command)
    command = ['touch', '%s/data.tgz' % BACKUP_DIR]
    sysutils.send_command(command)
    command = ['touch', '%s/db.tgz' % BACKUP_DIR]
    sysutils.send_command(command)
    command = ['/usr/sbin/logrotate', '-f', '/etc/logrotate.d/xivo-backup']
    sysutils.send_command(command)

    expected_files = ['data.tgz', 'data.tgz.1', 'db.tgz', 'db.tgz.1']
    for expected_file in expected_files:
        assert sysutils.path_exists('%s/%s' % (BACKUP_DIR, expected_file))

    command = ['/usr/sbin/logrotate', '-f', '/etc/logrotate.d/xivo-backup']
    sysutils.send_command(command)

    expected_files.extend(['data.tgz.2', 'db.tgz.2'])
    for expected_file in expected_files:
        assert sysutils.path_exists('%s/%s' % (BACKUP_DIR, expected_file))


def _get_asterisk_pid():
    return sysutils.get_content_file('/var/run/asterisk/asterisk.pid')


@step(u'Then max open file descriptors are equals to 8192')
def then_max_open_file_descriptors_are_equals_to_8192(step):
        pid = _get_asterisk_pid().strip()
        cmd = ['grep', '\'Max open files\'', '/proc/%s/limits' % pid]
        string_limit = sysutils.output_command(cmd)
        limit = re.sub('\s+', ' ', string_limit).split()[3]
        assert_that(int(limit), equal_to(8192))


@step(u'Then sources.list points on the mirror "([^"]*)"')
def then_sources_list_points_on_the_mirror(step, mirror):
    mirror_line = "deb %s wheezy main" % mirror
    source_line = "deb-src %s wheezy main" % mirror

    file_contents = sysutils.get_content_file('/etc/apt/sources.list').strip()
    lines = [l.strip() for l in file_contents.splitlines() if l.strip()]

    assert_that(lines, has_items(mirror_line, source_line))
