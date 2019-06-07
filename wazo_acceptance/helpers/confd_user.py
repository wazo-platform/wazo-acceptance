# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later


class ConfdUser:

    def __init__(self, context):
        self._context = context
        self._confd_client = context.confd_client

    def create(self, body):
        user = self._confd_client.users.create(body)
        self._context.add_cleanup(self._confd_client.users.delete, user)
        return user

    def add_line(self, user, line):
        self._confd_client.users(user).add_line(line)
        self._context.add_cleanup(self._confd_client.users(user).remove_line, line)
