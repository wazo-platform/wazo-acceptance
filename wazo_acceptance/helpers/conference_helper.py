# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later


class ConferenceHelper:

    def __init__(self, context):
        self._context = context
        self._confd_client = context.confd_client

    def add_extension(self, conference, extension):
        self._confd_client.conferences(conference).add_extension(extension)
        self._context.add_cleanup(
            self._confd_client.conferences(conference).remove_extension,
            extension,
        )

    def create(self, name):
        conference = self._confd_client.conferences.create({'name': name})
        self._context.add_cleanup(self._confd_client.conferences.delete, conference)
        return conference
