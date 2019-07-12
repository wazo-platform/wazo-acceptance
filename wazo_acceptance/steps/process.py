# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from behave import then


@then(u'the service "{service_name}" is running')
def then_the_service_name_is_running(context, service_name):
    pidfile = context.remote_sysutils.get_pidfile_for_service_name(service_name)
    assert context.remote_sysutils.is_process_running(pidfile)
