# -*- coding: utf-8 -*-

# Copyright (C) 2013 Avencall
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

from hamcrest import *
from lettuce import world

from xivo_ws import Schedule


def add_schedule(name, timezone, times):
    delete_schedules_with_name(name)
    schedule = _create_schedule(name, timezone, times)
    world.ws.schedules.add(schedule)


def assert_schedule_exists(name, timezone, times):
    expected_schedule = _create_schedule(name, timezone, times)
    result_schedule = view_schedule(find_schedule_id_with_name(name))

    assert_that(result_schedule, equal_to(expected_schedule))


def _create_schedule(name, timezone, times):
    schedule = Schedule(
        name=name,
        timezone=timezone,
    )
    opened, closed = [], []
    for time in times:
        formatted_time = {
            'hours': '%s-%s' % (time['Start hour'], time['End hour']),
            'weekdays': time['Days of week'],
            'monthdays': time['Days of month'],
            'months': time['Months'],
        }
        if time['Status'] == 'Opened':
            opened.append(formatted_time)
        elif time['Status'] == 'Closed':
            closed.append(formatted_time)
    if opened:
        schedule.opened = opened
    if closed:
        schedule.closed = closed

    return schedule


def delete_schedules_with_name(name):
    for schedule in _search_schedules_with_name(name):
        world.ws.schedules.delete(schedule.id)


def find_schedule_id_with_name(name):
    schedule = _find_schedule_with_name(name)
    return schedule.id


def view_schedule(schedule_id):
    return world.ws.schedules.view(schedule_id)


def _find_schedule_with_name(name):
    schedules = _search_schedules_with_name(name)
    if len(schedules) != 1:
        raise Exception('expecting 1 schedule with name %r: found %s' %
                        (name, len(schedules)))
    return schedules[0]


def _search_schedules_with_name(name):
    name = unicode(name)
    schedules = world.ws.schedules.list()
    return [schedule for schedule in schedules if schedule.name == name]
