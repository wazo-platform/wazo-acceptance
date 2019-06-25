# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later


class Incall:

    def __init__(self, context):
        self._context = context
        self._confd_client = context.confd_client

    def create(self, body):
        incall = self._confd_client.incalls.create(body)
        self._context.add_cleanup(self._confd_client.incalls.delete, incall)
        return incall

    def add_extension(self, incall, extension):
        with self._context.helpers.bus.wait_for_dialplan_reload():
            self._confd_client.incalls(incall).add_extension(extension)
        self._context.add_cleanup(self._confd_client.incalls(incall).remove_extension, extension)
