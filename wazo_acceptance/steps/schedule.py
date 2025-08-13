# Copyright 2019-2025 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from behave import given


def _expand_number_ranges(collapsed):
    numbers = []
    for range_bloc in collapsed.split(','):
        if '-' in range_bloc:
            low, high = map(int, range_bloc.split('-'))
            numbers += range(low, high + 1)
        else:
            numbers.append(int(range_bloc))
    return numbers


def _table_to_body(context, name, timezone, table, destination=None):
    schedule = {
        'name': name,
        'timezone': timezone,
        'open_periods': [],
        'exceptional_periods': [],
        'closed_destination': {
            'type': 'none'
        },
    }
    if destination:
        schedule['closed_destination'] = destination

    context.table.require_columns([
        'periods', 'months', 'month_days', 'week_days', 'hours_start', 'hours_end'
    ])
    for row in table:
        time = row.as_dict()

        period = {
            'hours_end': time['hours_end'],
            'hours_start': time['hours_start'],
            'month_days': _expand_number_ranges(time['month_days']),
            'months': _expand_number_ranges(time['months']),
            'week_days': _expand_number_ranges(time['week_days']),
            'destination': {'type': 'none'}
        }

        if time.get('destination_user'):
            firstname, lastname = time['destination_user'].split(" ")
            confd_user = context.helpers.confd_user.get_by(firtname=firstname, lastname=lastname)
            period['destination'] = {'type': 'user', 'user_id': confd_user['id']}

        schedule["%s_periods" % time['periods']].append(period)

    return schedule


@given('I have a schedule "{name}" in "{timezone}" with the following schedules:')
def given_i_have_a_schedule_in_certain_timezeon_with_the_following_schedules(context, name, timezone):
    context.helpers.schedule.create(_table_to_body(context, name, timezone, context.table))


@given('I have a schedule "{name}" in "{timezone}" with the following schedules towards user "{firstname} {lastname}":')
def given_i_have_a_schedule_in_timezone_towards_a_user_with_the_following_schedules(context, name, timezone, firstname, lastname):
    confd_user = context.helpers.confd_user.get_by(firtname=firstname, lastname=lastname)
    destination = {'type': 'user', 'user_id': confd_user['id']}
    context.helpers.schedule.create(_table_to_body(context, name, timezone, context.table, destination))


@given('I have a schedule "{name}" associated to incall "{exten}@{exten_context}"')
def givent_i_have_a_schedule_associated_to_incall(context, name, exten, exten_context):
    context_name = context.helpers.context.get_by(label=exten_context)['name']
    extension = context.helpers.extension.get_by(exten=exten, context=context_name)
    schedule = context.helpers.schedule.get_by(name=name)
    context.confd_client.incalls(extension['incall']).add_schedule(schedule)
