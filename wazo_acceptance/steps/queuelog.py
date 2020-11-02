# Copyright 2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from behave import given, then


@given('there is no queue_log for queue "{queue_name}"')
def no_queue_log_for_queue_1(context, queue_name):
    context.ssh_client.check_call(['queue-log-clear-one-queue.sh', queue_name])


@then('queue_log contains {expected_count} "{event_name}" events for queue "{queue_name}"')
def queue_log_contains_1_2_events_for_queue_3(context, expected_count, event_name, queue_name):
    actual_count = context.ssh_client.out_call(['queue-log-count-queue-events.sh', queue_name, event_name]).strip()
    assert actual_count == expected_count, f'expected {repr(expected_count)}, got {repr(actual_count)}'
