# Copyright 2019-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later


class Conference:

    def __init__(self, context):
        self._context = context
        self._confd_client = context.confd_client

    def create(self, body):
        modules = {'confbridge': True}
        wait_reload = self._context.helpers.bus.wait_for_asterisk_reload
        with wait_reload(**modules):
            conference = self._confd_client.conferences.create(body)

        delete = self._confd_client.conferences.delete
        self._context.add_cleanup(wait_reload(**modules)(delete), conference)
        return conference

    def add_extension(self, conference, extension):
        modules = {'dialplan': True}
        wait_reload = self._context.helpers.bus.wait_for_asterisk_reload
        with wait_reload(**modules):
            self._confd_client.conferences(conference).add_extension(extension)

        remove = self._confd_client.conferences(conference).remove_extension
        self._context.add_cleanup(wait_reload(**modules)(remove), extension)
