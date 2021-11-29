# Copyright 2021 The Wazo Authors  (see the AUTHORS file)
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
        with self._context.helpers.bus.wait_for_asterisk_reload(dialplan=True):
            self._confd_client.outcalls(outcall).add_extension(extension)
        self._context.add_cleanup(self._confd_client.outcalls(outcall).remove_extension, extension)

    def add_trunk(self, outcall, trunk):
        with self._context.helpers.bus.wait_for_asterisk_reload(dialplan=True):
            trunks = self._confd_client.outcalls.get(outcall)['trunks']
            new_trunks = [{'id': trunk['id']}, *trunks]
            self._confd_client.outcalls(outcall).update_trunks(new_trunks)
        self._context.add_cleanup(self._confd_client.outcalls(outcall).update_trunks, trunks)

    def get_by(self, **kwargs):
        user = self._find_by(**kwargs)
        if not user:
            raise Exception('Confd outcall not found: {}'.format(kwargs))
        return user

    def _find_by(self, **kwargs):
        users = self._confd_client.outcalls.list(**kwargs)['items']
        for user in users:
            return user
