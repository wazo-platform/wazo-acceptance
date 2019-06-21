# -*- coding: utf-8 -*-
# Copyright 2013-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from behave import given


@given('there are pickups')
def given_there_are_pickup(context):
    for row in context.table:
        data = row.as_dict()
        pickup_args = {
            'name': data['name']
        }
        with context.helpers.bus.wait_for_dialplan_reload():
            call_pickup = context.helpers.pickup.create(pickup_args)

            user = _find_user_by_name(context, data.get('user_interceptor'))
            if user:
                context.helpers.pickup.update_user_interceptors(call_pickup, user)

            group = _find_group_by_name(context, data.get('group_interceptor'))
            if group:
                context.helpers.pickup.update_group_interceptors(call_pickup, group)

            user = _find_user_by_name(context, data.get('user_target'))
            if user:
                context.helpers.pickup.update_user_targets(call_pickup, user)

            group = _find_group_by_name(context, data.get('group_target'))
            if group:
                context.helpers.pickup.update_group_targets(call_pickup, group)


def _find_group_by_name(context, name):
    if not name:
        return

    return context.helpers.confd_group.get_by(name=name)


def _find_user_by_name(context, name):
    if not name:
        return name

    firstname, lastname = name.split()
    return context.helpers.user.get_by(firstname=firstname, lastname=lastname)
