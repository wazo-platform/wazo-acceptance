# Copyright 2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from behave import given, when, then


@given('there is no queue_log for queue "{queue_name}"')
def given_no_queue_log_for_queue_1(context, queue_name):
    context.ssh_client.check_call(['queue-log-clear-one-queue.sh', queue_name])


@given('there are corrupt entries in queue_log')
def given_corrupt_entries_in_queue_log(context):
    context.ssh_client.check_call(['queue-log-insert-corrupt-entries.sh'])


@when('I execute the command wazo-stat')
def when_execute_the_command_wazo_stat(context):
    context.wazo_stat_result = context.ssh_client.call(['wazo-stat'])


@then('queue_log contains {expected_count} "{event_name}" events for queue "{queue_name}"')
def then_queue_log_contains_1_2_events_for_queue_3(context, expected_count, event_name, queue_name):
    actual_count = context.ssh_client.out_call(['queue-log-count-queue-events.sh', queue_name, event_name]).strip()
    assert actual_count == expected_count, f'expected {repr(expected_count)}, got {repr(actual_count)}'


@then('the command wazo-stat did not return any error')
def then_command_wazo_stat_did_not_return_any_error(context):
    assert context.wazo_stat_result == 0, f"wazo-stat return code was {context.wazo_stat_result}"
