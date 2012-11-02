# -*- coding: utf-8 -*-

from lettuce import world
from xivo_ws import Incall, UserDestination, OverwriteCallerIDMode
from xivo_lettuce.manager_ws import user_manager_ws


def add_incall(number, context, dst_type, dst_name, caller_id=None):
    incall = Incall()
    incall.number = number
    incall.context = context
    incall.destination = _new_destination(dst_type, dst_name)
    if caller_id:
        incall.caller_id_mode = OverwriteCallerIDMode(caller_id)
    world.ws.incalls.add(incall)


def _new_destination(dst_type, dst_name):
    if dst_type == 'user':
        return _new_user_destination(dst_name)
    else:
        raise Exception('unknown destination type %r' % dst_type)


def _new_user_destination(fullname):
    firstname, lastname = fullname.split()
    user_id = user_manager_ws.find_user_id_with_firstname_lastname(firstname, lastname)
    return UserDestination(user_id)


def delete_incalls_with_did(incall_did):
    incalls = world.ws.incalls.search_by_number(incall_did)
    for incall in incalls:
        world.ws.incalls.delete(incall.id)
