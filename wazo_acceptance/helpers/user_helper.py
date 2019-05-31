# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later


class UserHelper:

    def __init__(self, context):
        self._context = context
        self._auth_client = context.auth_client

    def create(self, body):
        user = self._auth_client.users.new(**body)
        self._context.add_cleanup(self._auth_client.users.delete, user['uuid'])
        return user
