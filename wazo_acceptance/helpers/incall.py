# Copyright 2019-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later


class Incall:

    def __init__(self, context):
        self._context = context
        self._confd_client = context.confd_client

    def create(self, body):
        incall = self._confd_client.incalls.create(body)
        self._context.add_cleanup(self._confd_client.incalls.delete, incall)
        return incall

    def add_extension(self, incall, extension):
        modules = {'dialplan': True}
        wait_reload = self._context.helpers.bus.wait_for_asterisk_reload
        with wait_reload(**modules):
            self._confd_client.incalls(incall).add_extension(extension)

        remove = self._confd_client.incalls(incall).remove_extension
        self._context.add_cleanup(wait_reload(**modules)(remove), extension)

    def get_by(self, **kwargs):
        user = self._find_by(**kwargs)
        if not user:
            raise Exception(f'Confd incall not found: {kwargs}')
        return user

    def _find_by(self, **kwargs):
        users = self._confd_client.incalls.list(**kwargs)['items']
        for user in users:
            return user
