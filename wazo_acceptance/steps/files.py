# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import os
import re

from hamcrest import (
    assert_that,
    is_not,
    none,
)
from behave import then, given

BACKUP_DIR = '/var/backups/xivo'


@then('the mirror list contains a line matching "{mirror}"')
def then_the_mirror_list_contains_a_line_matching_mirror(context, mirror):
    match = _match_on_mirror_list(context, mirror)
    assert_that(match, is_not(none()))


def _match_on_mirror_list(context, regex):
    output = context.remote_sysutils.output_command(['apt-cache', 'policy'])
    return re.search(regex, output)


@given('there are backup files')
def given_there_are_backup_files(context):
    backuped_files = [
        os.path.join(BACKUP_DIR, 'data.tgz'),
        os.path.join(BACKUP_DIR, 'db.tgz'),
    ]

    for file_ in backuped_files:
        context.remote_sysutils.send_command(['rm', '-f', '{file_}*'.format(file_=file_)])
        context.remote_sysutils.send_command(['touch', file_])

@then('backup files successfully rotated')
def then_backup_files_successfully_rotated(context):
    rotated_files = [
        os.path.join(BACKUP_DIR, 'data.tgz.{num}'),
        os.path.join(BACKUP_DIR, 'db.tgz.{num}'),
    ]

    context.remote_sysutils.send_command(
        ['/usr/sbin/logrotate', '-f', '/etc/logrotate.d/xivo-backup']
    )

    expected_files = [file_.format(num='1') for file_ in rotated_files]
    for expected_file in expected_files:
        assert context.remote_sysutils.path_exists(expected_file)

    context.remote_sysutils.send_command(
        ['/usr/sbin/logrotate', '-f', '/etc/logrotate.d/xivo-backup']
    )

    expected_files = [file_.format(num='2') for file_ in rotated_files]
    for expected_file in expected_files:
        assert context.remote_sysutils.path_exists(expected_file)
