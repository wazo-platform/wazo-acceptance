# Copyright 2019-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later


class ParkingLot:

    def __init__(self, context):
        self._context = context
        self._confd_client = context.confd_client

    def create(self, body):
        modules = {'parking': True}
        wait_reload = self._context.helpers.bus.wait_for_asterisk_reload
        with wait_reload(**modules):
            parking_lot = self._confd_client.parking_lots.create(body)

        delete = self._confd_client.parking_lots.delete
        self._context.add_cleanup(wait_reload(**modules)(delete), parking_lot)
        return parking_lot

    def add_extension(self, parking_lot, extension):
        self._context.confd_client.parking_lots(parking_lot).add_extension(extension)
        self._context.add_cleanup(
            self._confd_client.parking_lots(parking_lot).remove_extension,
            extension
        )
