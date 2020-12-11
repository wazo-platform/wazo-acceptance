# Copyright 2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from behave import when


@when('I execute the logrotate command for service "{service}"')
def when_i_execute_logrotate_for_service(context, service):
    command = '/usr/sbin/logrotate -f /etc/logrotate.d/{}'.format(service)
    context.ssh_client.check_call([command])
