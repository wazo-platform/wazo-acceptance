# -*- coding: utf-8 -*-
# Copyright 2013-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from lettuce import step, world


@step(u'Given there are pickups:$')
def given_there_are_pickup(step):
    for data in step.hashes:
        _delete_pickup(data['name'])
        pickup_args = {
            'name': data['name']
        }
        call_pickup = world.confd_client.call_pickups.create(pickup_args)

        user = _find_user_by_firstname(data.get('user_interceptor'))
        if user:
            world.confd_client.call_pickups(call_pickup['id']).update_user_interceptors([user])

        group = _find_group_by_name(data.get('group_interceptor'))
        if group:
            world.confd_client.call_pickups(call_pickup['id']).update_group_interceptors([group])

        user = _find_user_by_firstname(data.get('user_target'))
        if user:
            world.confd_client.call_pickups(call_pickup['id']).update_user_targets([user])

        group = _find_group_by_name(data.get('group_target'))
        if group:
            world.confd_client.call_pickups(call_pickup['id']).update_group_targets([group])


def _delete_pickup(name):
    call_pickups = world.confd_client.call_pickups.list(name=name)['items']
    for call_pickup in call_pickups:
        world.confd_client.call_pickups.delete(call_pickup['id'])


def _find_user_by_firstname(firstname):
    if not firstname:
        return

    users = world.confd_client.users.list(firstname=firstname)['items']
    for user in users:
        # cannot search by empty/none lastname with confd
        if user['lastname']:
            continue

        return user


def _find_group_by_name(name):
    if not name:
        return

    groups = world.confd_client.groups.list(name=name)['items']
    for group in groups:
        return group
