# Copyright 2019-2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import os
import re

from behave import then, given
from hamcrest import (
    assert_that,
    contains_string,
    equal_to,
    is_,
    is_not,
    none,
)

BACKUP_DIR = '/var/backups/xivo'
ASTERISK_VM_PATH = '/var/spool/asterisk/voicemail'
MOH_PATH = '/usr/share/asterisk/moh/default'
ASTERISK_SOUND_PATH = '/usr/share/asterisk/sounds/en'


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
        context.remote_sysutils.send_command(['touch', file_])
        context.add_cleanup(
            context.remote_sysutils.send_command,
            ['rm', '-f', '{file_}'.format(file_=file_)]
        )


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
        context.add_cleanup(
            context.remote_sysutils.send_command,
            ['rm', '-f', '{expected_file}'.format(expected_file=expected_file)]
        )

    context.remote_sysutils.send_command(
        ['/usr/sbin/logrotate', '-f', '/etc/logrotate.d/xivo-backup']
    )

    expected_files = [file_.format(num='2') for file_ in rotated_files]
    for expected_file in expected_files:
        assert context.remote_sysutils.path_exists(expected_file)
        context.add_cleanup(
            context.remote_sysutils.send_command,
            ['rm', '-f', '{expected_file}'.format(expected_file=expected_file)]
        )


@then('the file "{file_name}" does not exist on "{instance}"')
def then_the_file_filename_does_not_exist(context, file_name, instance):
    context = getattr(context.instances, instance)
    assert_that(context.remote_sysutils.path_exists(file_name), is_(False))


@then('there are cron jobs in "{file_name}" on "{instance}"')
def then_there_are_cron_jobs_in_file_name_on_instance(context, file_name, instance):
    step_context = context
    instance_context = getattr(context.instances, instance)
    file_content = instance_context.remote_sysutils.get_content_file(file_name)
    for row in step_context.table:
        expected_line = row['cron job']
        expected_line = expected_line.replace(
            '{{ slave_voip_ip_address }}',
            instance_context.wazo_config.get('slave_host') or '<unknown>',
        )
        expected_line = expected_line.replace(
            '{{ master_voip_ip_address }}',
            instance_context.wazo_config.get('master_host') or '<unknown>',
        )
        assert_that(file_content, contains_string(expected_line))


@then('Asterisk may open at most "{max_file_descriptors}" file descriptors')
def then_asterisk_may_open_at_most_max_file_descriptors(context, max_file_descriptors):
    limit_number_of_file = context.remote_sysutils.process_limitnofile('asterisk')
    assert_that(limit_number_of_file, equal_to('8192'))


@then('Asterisk sound files are correctly installed')
def then_asterisk_sound_files_correctly_installed(context):
    assert not context.remote_sysutils.dir_is_empty(ASTERISK_SOUND_PATH)


@then('MOH files are owned by asterisk:www-data')
def then_moh_files_are_owned_by_asterisk_www_data(context):
    command = ['apt-get', 'install', '-y', 'asterisk-moh-opsound-wav']
    context.remote_sysutils.send_command(command)
    text = context.remote_sysutils.get_list_file(MOH_PATH)
    lines = text.split("\n")
    for line in lines:
        if not line:
            continue
        file_ = '{}/{}'.format(MOH_PATH, line.strip())
        assert context.remote_sysutils.file_owned_by_user(file_, 'asterisk')
        assert context.remote_sysutils.file_owned_by_group(file_, 'www-data')


@given('the file "{path}" is empty')
def given_the_file_is_empty(context, path):
    # if the file already exist on the fs, it will be truncated to 0
    context.ssh_client.check_call(['truncate', '-s0', path])


@then('the file "{path}" is not empty')
def then_the_file_is_not_empty(context, path):
    command = ['stat', '-c', '%s', path]
    output = context.remote_sysutils.output_command(command).strip()
    assert int(output) > 0
