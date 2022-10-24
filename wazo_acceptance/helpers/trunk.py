# Copyright 2019-2022 The Wazo Authors  (see the AUTHORS file)
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
        modules = {'pjsip': True}
        wait_reload = self._context.helpers.bus.wait_for_asterisk_reload
        with wait_reload(**modules):
            self._confd_client.trunks(trunk).add_endpoint_sip(sip)

        remove = self._confd_client.trunks(trunk).remove_endpoint_sip
        self._context.add_cleanup(wait_reload(**modules)(remove), sip)
