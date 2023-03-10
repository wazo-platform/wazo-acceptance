# Copyright 2019-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from behave import then


@then('the service "{service_name}" is running')
def then_the_service_name_is_running(context, service_name):
    assert context.remote_sysutils.is_process_running(service_name)


@then('the service "{service_name}" has priority "{priority}"')
def then_the_service_name_has_priority(context, service_name, priority):
    actual_priority = context.remote_sysutils.process_priority('asterisk')
    assert actual_priority == priority, f'{actual_priority=} is not equal to {priority=}'
