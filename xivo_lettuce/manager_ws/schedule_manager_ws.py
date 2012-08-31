# -*- coding: utf-8 -*-

from lettuce.registry import world
from xivo_ws import Schedule


def get_schedule_id_with_name(name):
    schedules = world.ws.schedules.list()
    for schedule in schedules:
        if schedule.name == str(name):
            return schedule.id
    raise Exception('no schedule with name %s' % name)


def delete_schedule_with_name(name):
    try:
        world.ws.schedules.delete(get_schedule_id_with_name(name))
    except Exception:
        pass


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
