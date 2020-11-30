# Copyright 2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

class CallPermission:

    def __init__(self, context):
        self._context = context
        self._confd_client = context.confd_client

    def create(self, body):
        call_permission = self._confd_client.call_permissions.create(body)
        self._context.add_cleanup(self._confd_client.call_permissions.delete, call_permission)
        return call_permission
