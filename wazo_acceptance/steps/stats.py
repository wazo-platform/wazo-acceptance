# Copyright 2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from behave import when, then
from datetime import datetime


@when('I generate contact center stats')
def when_generate_contact_center_stats(context):
    context.ssh_client.check_call(['wazo-stat fill_db'])


@then('contact center stats for queue "{queue_name}" in the current hour are')
def then_contact_center_stats_for_queue_1(context, queue_name):
    now = datetime.now()
    last_hour = datetime(now.year, now.month, now.day, now.hour, 0, 0)

    queue_id = context.helpers.queue.find_by(name=queue_name)['id']
    queue_stats = context.call_logd_client.queue_statistics.get_by_id(
        queue_id=queue_id, from_=last_hour.isoformat(),
    )
    total_stats = queue_stats['items'][-1]

    for row in context.table:
        expected_stats = row.as_dict()

    for stat_name, expected_value in expected_stats.items():
        expected_value = float(expected_value)
        actual_value = total_stats[stat_name]
        assert actual_value == expected_value, \
            f'expected {stat_name} = {expected_value}, got {actual_value}'
