# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later


class ConfdGroup:

    def __init__(self, context):
        self._context = context
        self._confd_client = context.confd_client

    def create(self, body):
        timeout = body.pop('timeout', None)
        if timeout:
            body['timeout'] = int(timeout)

        with self._context.helpers.bus.wait_for_asterisk_reload(queue=True):
            group = self._confd_client.groups.create(body)
        self._context.add_cleanup(self._confd_client.groups.delete, group)
        return group

    def get_by(self, **kwargs):
        group = self._find_by(**kwargs)
        if not group:
            raise Exception('Group not found: {}'.format(kwargs))
        return group

    def _find_by(self, **kwargs):
        groups = self._confd_client.groups.list(**kwargs)['items']
        for group in groups:
            return group

    def add_extension(self, group, extension):
        self._confd_client.groups(group).add_extension(extension)
        self._context.add_cleanup(self._confd_client.groups(group).remove_extension, extension)

    def update_fallbacks(self, group, fallbacks):
        self._confd_client.groups(group).update_fallbacks(fallbacks)

    def update_user_members(self, group, users):
        self._confd_client.groups(group).update_user_members(users)
