# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later


class Pickup:

    def __init__(self, context):
        self._context = context
        self._confd_client = context.confd_client

    def create(self, pickup_args):
        call_pickup = self._confd_client.call_pickups.create(pickup_args)
        self._context.add_cleanup(self._confd_client.call_pickups.delete, call_pickup)
        return call_pickup
