# Copyright 2021-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later


class Outcall:

    def __init__(self, context):
        self._context = context
        self._confd_client = context.confd_client

    def create(self, body):
        outcall = self._confd_client.outcalls.create(body)
        self._context.add_cleanup(self._confd_client.outcalls.delete, outcall)
        return outcall

    def add_extension(self, outcall, extension):
        modules = {'dialplan': True}
        wait_reload = self._context.helpers.bus.wait_for_asterisk_reload
        with wait_reload(**modules):
            self._confd_client.outcalls(outcall).add_extension(extension)

        remove = self._confd_client.outcalls(outcall).remove_extension
        self._context.add_cleanup(wait_reload(**modules)(remove), extension)

    def add_trunk(self, outcall, trunk):
        modules = {'dialplan': True}
        wait_reload = self._context.helpers.bus.wait_for_asterisk_reload
        with wait_reload(**modules):
            trunks = self._confd_client.outcalls.get(outcall)['trunks']
            new_trunks = [{'id': trunk['id']}, *trunks]
            self._confd_client.outcalls(outcall).update_trunks(new_trunks)

        update = self._confd_client.outcalls(outcall).update_trunks
        self._context.add_cleanup(wait_reload(**modules)(update), trunks)

    def get_by(self, **kwargs):
        outcall = self._find_by(**kwargs)
        if not outcall:
            raise Exception(f'Confd outcall not found: {kwargs}')
        return outcall

    def _find_by(self, **kwargs):
        outcalls = self._confd_client.outcalls.list(**kwargs)['items']
        for outcall in outcalls:
            return outcall
