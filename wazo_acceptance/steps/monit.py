# Copyright 2019-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from wazo_test_helpers import until

from behave import then


@then('monit monitors the service "{process_name}"')
def then_monit_monitors_the_service_process_name(context, process_name):
    until.true(
        context.helpers.monit.process_monitored, process_name,
        timeout=60,
        message=f'Monit did not monitor process {process_name}',
    )


@then('monit does not monitor the service "{process_name}"')
def then_monit_does_not_monitor_the_service_process_name(context, process_name):
    until.false(
        context.helpers.monit.process_monitored, process_name,
        timeout=60,
        message=f'Monit is still monitoring process {process_name}',
    )
