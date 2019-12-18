# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later


class ParkingLot:

    def __init__(self, context):
        self._context = context
        self._confd_client = context.confd_client

    def create(self, body):
        with self._context.helpers.bus.wait_for_asterisk_reload(parking=True):
            parking_lot = self._confd_client.parking_lots.create(body)
        self._context.add_cleanup(self._confd_client.parking_lots.delete, parking_lot)
        return parking_lot

    def add_extension(self, parking_lot, extension):
        self._context.confd_client.parking_lots(parking_lot).add_extension(extension)
        self._context.add_cleanup(
            self._confd_client.parking_lots(parking_lot).remove_extension,
            extension
        )
