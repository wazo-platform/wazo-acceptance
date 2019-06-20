# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later


class Pickup:

    def __init__(self, context):
        self._context = context
        self._confd_client = context.confd_client

    def create(self, pickup_args):
        call_pickup = self._confd_client.call_pickups.create(pickup_args)
        self._context.add_cleanup(self._confd_client.call_pickups.delete, call_pickup['id'])
        return call_pickup

    def update_user_interceptors(self, pickup, user):
        self._confd_client.call_pickups(pickup['id']).update_user_interceptors([user])

    def update_group_interceptors(self, pickup, group):
        self._confd_client.call_pickups(pickup['id']).update_group_interceptors([group])

    def update_user_targets(self, pickup, user):
        self._confd_client.call_pickups(pickup['id']).update_user_targets([user])

    def update_group_targets(self, pickup, group):
        self._confd_client.call_pickups(pickup['id']).update_group_targets([group])
