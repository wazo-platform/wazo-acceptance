# Copyright 2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

class CallPermission:

    def __init__(self, context):
        self._context = context
        self._confd_client = context.confd_client

    def add_user(self, call_permission, user):
        self._confd_client.call_permissions(call_permission).add_user(user)
        self._context.add_cleanup(
            self._confd_client.call_permissions(call_permission).remove_user,
            user,
        )

    def create(self, body):
        call_permission = self._confd_client.call_permissions.create(body)
        self._context.add_cleanup(self._confd_client.call_permissions.delete, call_permission)
        return call_permission
