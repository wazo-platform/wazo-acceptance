# Copyright 2013-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from behave import when


@when('I restart "{service_name}"')
def i_restart_service(context, service_name):
    context.remote_sysutils.restart_service(service_name)
