# Copyright 2020-2026 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import logging
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

from behave import then, when

logger = logging.getLogger(__name__)


@when('I generate contact center stats')
def when_generate_contact_center_stats(context):
    now = datetime.now(tz=timezone.utc)
    # NOTE: Add one second to include calls from the current second
    end = now + timedelta(seconds=1)
    end_arg = end.strftime('%Y-%m-%dT%H:%M:%S%z')
    command = ['wazo-stat', 'fill_db', f'--end={end_arg}']
    std_out_err = context.ssh_client.out_err_call(command)
    logger.debug(std_out_err)


@then('contact center stats for queue "{queue_name}" in the current hour are:')
def then_contact_center_stats_for_queue_1(context, queue_name):
    tz = ZoneInfo('America/Montreal')
    now = datetime.now(tz=tz)
    last_hour = datetime(now.year, now.month, now.day, now.hour, 0, 0)

    queue_id = context.helpers.queue.find_by(name=queue_name)['id']
    queue_stats = context.call_logd_client.queue_statistics.get_by_id(
        queue_id=queue_id, from_=last_hour.isoformat(), timezone=str(tz)
    )
    total_stats = queue_stats['items'][-1]

    for row in context.table:
        expected_stats = row.as_dict()

    for stat_name, expected_value in expected_stats.items():
        expected_value = float(expected_value)
        actual_value = total_stats[stat_name]
        msg = f'expected {stat_name} = {expected_value}, got {actual_value}'
        assert actual_value == expected_value, msg


@then('contact center stats for agent "{agent_number}" in the current hour are:')
def then_contact_center_stats_for_agent(context, agent_number):
    tz = ZoneInfo('America/Montreal')
    now = datetime.now(tz=tz)
    last_hour = datetime(now.year, now.month, now.day, now.hour, 0, 0)

    agent_id = context.helpers.agent.get_by(number=agent_number)['id']
    agent_stats = context.call_logd_client.agent_statistics.get_by_id(
        agent_id=agent_id,
        from_=last_hour.isoformat(),
        timezone=str(tz),
    )
    total_stats = agent_stats['items'][-1]

    for row in context.table:
        expected_stats = row.as_dict()

    for stat_name, expected_value in expected_stats.items():
        lower_bound, higher_bound = _parse_seconds_range(expected_value)
        actual_value = total_stats[stat_name]
        msg = f'expected {stat_name} to be between {lower_bound} and {higher_bound}, got {actual_value}'
        assert lower_bound <= actual_value <= higher_bound, msg


def _parse_seconds_range(value):
    lower_bound, _, higher_bound = value.partition('..')
    return int(lower_bound), int(higher_bound or lower_bound)


@then('contact center qos stats for queue "{queue_name}" in the current hour are:')
def then_contact_center_qos_stats_for_queue_1(context, queue_name):
    thresholds = [row['qos_threshold'] for row in context.table if row['qos_threshold'] != 'remainder']
    tz = ZoneInfo('America/Montreal')
    now = datetime.now(tz=tz)
    last_hour = datetime(now.year, now.month, now.day, now.hour, 0, 0)
    queue_id = context.helpers.queue.find_by(name=queue_name)['id']
    queue_stats = context.call_logd_client.queue_statistics.get_qos_by_id(
        queue_id=queue_id,
        from_=last_hour.isoformat(),
        timezone=str(tz),
        qos_thresholds=','.join(thresholds)
    )
    total_stats = queue_stats['items'][-1]

    results = {str(threshold['max']): threshold for threshold in total_stats['quality_of_service']}
    results['remainder'] = results.pop('None')

    for row in context.table:
        expected = row.as_dict()
        expected['answered'] = int(expected['answered'])
        expected['abandoned'] = int(expected['abandoned'])
        actual = results[row['qos_threshold']]

        msg = f'qos {expected["qos_threshold"]}: expected {expected["abandoned"]}, got {actual["abandoned"]} abandoned calls'
        assert actual['abandoned'] == expected['abandoned'], msg
        msg = f'qos {expected["qos_threshold"]}: expected {expected["answered"]}, got {actual["answered"]} answered calls'
        assert actual['answered'] == expected['answered'], msg
