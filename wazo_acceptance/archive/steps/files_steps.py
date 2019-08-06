# -*- coding: utf-8 -*-
# Copyright 2013-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import os
import re

from hamcrest import assert_that
from hamcrest import contains_string
from hamcrest import is_not
from hamcrest import none
from lettuce import step, world

from xivo_acceptance.lettuce import sysutils


BACKUP_DIR = '/var/backups/xivo'


@step(u'Then backup files successfully rotated')
def then_backup_files_successfully_rotated(step):
    backuped_files = [os.path.join(BACKUP_DIR, 'data.tgz'),
                      os.path.join(BACKUP_DIR, 'db.tgz')]
    rotated_files = [os.path.join(BACKUP_DIR, 'data.tgz.{num}'),
                     os.path.join(BACKUP_DIR, 'db.tgz.{num}')]
    for file_ in backuped_files:
        sysutils.send_command(['rm', '-f', '{file_}*'.format(file_=file_)])
        sysutils.send_command(['touch', file_])

    sysutils.send_command(['/usr/sbin/logrotate', '-f', '/etc/logrotate.d/xivo-backup'])

    expected_files = backuped_files + [file_.format(num='1') for file_ in rotated_files]
    for expected_file in expected_files:
        assert sysutils.path_exists(expected_file)

    sysutils.send_command(['/usr/sbin/logrotate', '-f', '/etc/logrotate.d/xivo-backup'])

    expected_files = expected_files + [file_.format(num='2') for file_ in rotated_files]
    for expected_file in expected_files:
        assert sysutils.path_exists(expected_file)


@step(u'Then the mirror list contains a line matching "([^"]*)"')
def then_the_mirror_list_contains_a_line_matching_group1(step, regex):
    match = _match_on_mirror_list(regex)
    assert_that(match, is_not(none()))


def _match_on_mirror_list(regex):
    output = sysutils.output_command(['apt-cache', 'policy'])
    return re.search(regex, output)


@step(u'Then there are cron jobs in "([^"]*)":')
def then_there_are_cron_jobs_in_1(step, file_name):
    file_content = sysutils.get_content_file(file_name)
    for info in step.hashes:
        expected_line = info['cron job']
        expected_line = expected_line.replace('{{ slave_voip_ip_address }}', world.config.get('slave_host') or '<unknown>')
        expected_line = expected_line.replace('{{ master_voip_ip_address }}', world.config.get('master_host') or'<unknown>')
        assert_that(file_content, contains_string(expected_line))
