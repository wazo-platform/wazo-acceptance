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

from lettuce import world
from xivo_ws import Schedule


def add_schedule(name, opened=None):
    '''
    opened1 = {'hours': '00:00-00:01',
               'weekdays': '1-1',
               'monthdays': '1-1',
               'months': '1-1'
               },
               {...}
       }
   '''
    schedule = Schedule()
    schedule.name = name
    schedule.timezone = 'America/Montreal'
    if opened:
        schedule.opened = [opened]
    world.ws.schedules.add(schedule)


def delete_schedules_with_name(name):
    for schedule in _search_schedules_with_name(name):
        world.ws.schedules.delete(schedule.id)


def find_schedule_id_with_name(name):
    schedule = _find_schedule_with_name(name)
    return schedule.id


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
