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

    def enable_directed_extension(self, extension):
        pickup_feature = self._confd_client.extensions_features.list(search='pickup')['items'][0]
        new_pickup_feature = pickup_feature.copy()
        new_pickup_feature.update({
            'exten': '_{extension}.'.format(extension=extension),
            'enabled': True,
        })

        with self._context.helpers.bus.wait_for_asterisk_reload(pjsip=True):
            self._confd_client.extensions_features.update(new_pickup_feature)

        self._context.add_cleanup(self._confd_client.extensions_features.update, pickup_feature)
