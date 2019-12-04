# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later


class Conference:

    def __init__(self, context):
        self._context = context
        self._confd_client = context.confd_client

    def create(self, body):
        with self._context.helpers.bus.wait_for_asterisk_reload(confbridge=True):
            conference = self._confd_client.conferences.create(body)
        self._context.add_cleanup(self._confd_client.conferences.delete, conference)
        return conference

    def add_extension(self, conference, extension):
        with self._context.helpers.bus.wait_for_asterisk_reload(dialplan=True):
            self._confd_client.conferences(conference).add_extension(extension)
        self._context.add_cleanup(
            self._confd_client.conferences(conference).remove_extension,
            extension,
        )
