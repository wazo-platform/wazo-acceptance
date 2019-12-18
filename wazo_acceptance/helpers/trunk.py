# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later


class Trunk:

    def __init__(self, context):
        self._context = context
        self._confd_client = context.confd_client

    def create(self, body):
        trunk = self._confd_client.trunks.create(body)
        self._context.add_cleanup(self._confd_client.trunks.delete, trunk)
        return trunk

    def add_endpoint_sip(self, trunk, sip):
        self._confd_client.trunks(trunk).add_endpoint_sip(sip)
        self._context.add_cleanup(self._confd_client.trunks(trunk).remove_endpoint_sip, sip)
