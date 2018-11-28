# -*- coding: utf-8 -*-
# Copyright 2013-2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from hamcrest import assert_that
from hamcrest import has_entries
from lettuce import world

from xivo_acceptance.helpers import entity_helper


def add_schedule(name, timezone, times, destination=None):
    delete_schedules_with_name(name)
    schedule = _create_schedule(name, timezone, times, destination)
    world.confd_client.create(schedule)


def add_or_replace_schedule(data):
    delete_schedules_with_name(data['name'])
    entity = entity_helper.get_entity_with_name(data['entity'])
    if entity:
        tenant_uuid = entity['tenant_uuid']
    else:
        tenant_uuid = entity_helper.default_entity_id()['tenant_uuid']

    schedule = {
        'name': data['name'],
        'timezone': data.get('timezone', 'America/Montreal'),
    }
    world.confd_client.schedules.create(schedule, tenant_uuid=tenant_uuid)


def assert_schedule_exists(name, timezone, times):
    expected = _create_schedule(name, timezone, times)
    result = find_schedule_by(name=name)
    assert_that(result, has_entries(**expected))


def expand_number_ranges(collapsed):
    numbers = []
    for range_bloc in collapsed.split(','):
        if '-' in range_bloc:
            low, high = map(int, range_bloc.split('-'))
            numbers += range(low, high+1)
        else:
            numbers.append(int(range_bloc))
    return numbers


def _create_schedule(name, timezone, times, destination=None):
    schedule = {
        'name': name,
        'timezone': timezone,
        'closed_destination': {
            'type': 'none'
        }
    }
    if destination:
        schedule['closed_destination'] = destination

    opened, closed = [], []
    for time in times:
        period = {
            'hours_end': time['End hour'],
            'hours_start': time['Start hour'],
            'month_days': expand_number_ranges(time['Days of month']),
            'months': expand_number_ranges(time['Months']),
            'week_days': expand_number_ranges(time['Days of week']),
        }

        if time['Status'] == 'Opened':
            opened.append(period)
        elif time['Status'] == 'Closed':
            closed.append(period)

    schedule['open_periods'] = opened
    schedule['exceptional_periods'] = opened
    return schedule


def delete_schedules_with_name(name):
    schedules = world.confd_client.schedules.list(name=name)['items']
    for schedule in schedules:
        world.confd_client.delete(schedule['id'])


def get_schedule_by(**kwargs):
    schedule = find_schedule_by(**kwargs)
    if not schedule:
        raise Exception('Schedule not found: %s' % kwargs)
    return schedule


def find_schedule_by(**kwargs):
    schedules = world.confd_client.schedules.list(**kwargs)['items']
    for schedule in schedules:
        return schedule
