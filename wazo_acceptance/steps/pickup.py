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

        call_pickup = context.helpers.pickup.create(pickup_args)

        user = _find_user_by_name(context, data.get('user_interceptor'))
        if user:
            with context.helpers.bus.wait_for_asterisk_reload(pjsip=True):
                context.confd_client.call_pickups(call_pickup['id']).update_user_interceptors([user])

        group = _find_group_by_name(context, data.get('group_interceptor'))
        if group:
            with context.helpers.bus.wait_for_asterisk_reload(pjsip=True):
                context.confd_client.call_pickups(call_pickup['id']).update_group_interceptors([group])

        user = _find_user_by_name(context, data.get('user_target'))
        if user:
            with context.helpers.bus.wait_for_asterisk_reload(pjsip=True):
                context.confd_client.call_pickups(call_pickup['id']).update_user_targets([user])

        group = _find_group_by_name(context, data.get('group_target'))
        if group:
            with context.helpers.bus.wait_for_asterisk_reload(pjsip=True):
                context.confd_client.call_pickups(call_pickup['id']).update_group_targets([group])


@given('the direct pickup is enabled with "{extension}"')
def given_the_direct_pickup_is_enabled_with_extension(context, extension):
    context.helpers.pickup.enable_directed_extension(extension)


def _find_group_by_name(context, name):
    if not name:
        return

    return context.helpers.confd_group.get_by(name=name)


def _find_user_by_name(context, name):
    if not name:
        return

    firstname, lastname = name.split()
    return context.helpers.user.get_by(firstname=firstname, lastname=lastname)
