# Copyright 2019-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import os

from behave import when, then
from hamcrest import (
    assert_that,
    empty,
    is_,
    is_not,
)


@when('I generate a core dump')
def when_generate_core_dump(context):
    res = context.remote_sysutils.output_command(['ulimit -c 1024 && /usr/local/bin/wazo-crash-test'])
    separator = ': '
    for line in res.split('\n'):
        if separator not in line:
            continue
        name, value = line.split(separator, 1)
        if name == 'PID':
            context.pid = value
        elif name == 'Epoch time':
            context.epoch = value

    context.add_cleanup(
        context.remote_sysutils.output_command,
        ['rm', '-f', f'~/core.{context.pid}.{context.epoch}'],
    )


@then('there is a core dump file with a distinctive name')
def then_there_should_by_a_file(context):
    assert_that(context.pid, is_not(empty()))
    assert_that(context.epoch, is_not(empty()))

    filename = f'core.{context.pid}.{context.epoch}'
    path = os.path.join('~', filename)
    assert_that(
        context.remote_sysutils.path_exists(path), is_(True),
        f'No such file or directory {path}',
    )
