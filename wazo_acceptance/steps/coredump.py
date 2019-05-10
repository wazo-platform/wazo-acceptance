# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from behave import when


@when(u'I generate a core dump and remember the pid as "{pid}" and the epoch as "{epoch}"')
def generate_core_dump(context, pid, epoch):
    res = context.remote_sysutils.output_command(['ulimit -c 1024 && /usr/local/bin/core_dump'])
    separator = ': '
    for line in res.split('\n'):
        if separator not in line:
            continue
        name, value = line.split(separator, 1)
        if name == 'PID':
            setattr(context, pid, value)
        elif name == 'Epoch time':
            setattr(context, epoch, value)

    context.add_cleanup(
        context.remote_sysutils.output_command,
        ['rm', '-f', '~/core.{}.{}'.format(context.pid, context.epoch)],
    )
