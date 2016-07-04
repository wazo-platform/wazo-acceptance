# -*- coding: utf-8 -*-

# Copyright (C) 2013-2016 Avencall
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

from hamcrest import assert_that
from hamcrest import equal_to
from lettuce import world

from xivo_ws import Schedule
from xivo_acceptance.helpers import entity_helper
from xivo_acceptance.helpers import user_helper


class ScheduleDestination(object):
    pass


class ScheduleDestinationNone(ScheduleDestination):
    def to_ws_actiontype(self):
        return 'none'

    def to_ws_action_id(self):
        return ''

    def to_ws_action_args(self):
        return ''


class ScheduleDestinationUser(ScheduleDestination):
    def __init__(self, user_id):
        self.user_id = user_id

    def to_ws_actiontype(self):
        return 'user'

    def to_ws_action_id(self):
        return str(self.user_id)

    def to_ws_action_args(self):
        return ''

    @classmethod
    def from_name(cls, firstname, lastname):
        user_id = user_helper.get_user_id_with_firstname_lastname(firstname, lastname)
        return cls(user_id)


def add_schedule(name, timezone, times, destination=ScheduleDestinationNone()):
    delete_schedules_with_name(name)
    schedule = _create_schedule(name, timezone, times, destination)
    world.ws.schedules.add(schedule)


def add_or_replace_schedule(data):
    delete_schedules_with_name(data['name'])
    entity = entity_helper.get_entity_with_name(data['entity'])
    entity_id = entity.id if entity else entity_helper.default_entity_id()
    schedule = Schedule(
        entity_id=entity_id,
        name=data['name'],
        timezone=data.get('timezone', 'America/Montreal'),
    )
    world.ws.schedules.add(schedule)


def assert_schedule_exists(name, timezone, times, destination=ScheduleDestinationNone()):
    expected_schedule = _create_schedule(name, timezone, times, destination)
    result_schedule = view_schedule(find_schedule_id_with_name(name))

    assert_that(result_schedule, equal_to(expected_schedule))


def _create_schedule(name, timezone, times, fallback_destination):
    schedule = Schedule(
        entity_id=entity_helper.default_entity_id(),
        name=name,
        timezone=timezone,
        fallback_actiontype=fallback_destination.to_ws_actiontype(),
        fallback_action_destination_id=fallback_destination.to_ws_action_id(),
        fallback_action_destination_args=fallback_destination.to_ws_action_args(),
    )
    opened, closed = [], []
    for time in times:
        formatted_time = {
            'hours': '%s-%s' % (time['Start hour'], time['End hour']),
            'weekdays': time['Days of week'],
            'monthdays': time['Days of month'],
            'months': time['Months'],
        }
        destination = ScheduleDestinationNone()
        if time.get('Destination firstname') and time.get('Destination lastname'):
            destination = ScheduleDestinationUser.from_name(time['Destination firstname'], time['Destination lastname'])
        formatted_time['dialaction'] = {}
        formatted_time['dialaction']['actiontype'] = destination.to_ws_actiontype()
        formatted_time['dialaction']['actionarg1'] = destination.to_ws_action_id()
        formatted_time['dialaction']['actionarg2'] = destination.to_ws_action_args()
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
