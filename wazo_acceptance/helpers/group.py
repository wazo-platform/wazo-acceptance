# Copyright 2021 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later


class Group:

    def __init__(self, context):
        self._context = context
        self._confd_client = context.confd_client

    def add_extension(self, group, extension):
        with self._context.helpers.bus.wait_for_asterisk_reload(dialplan=True):
            self._context.confd_client.groups(group).add_extension(extension)
        self._context.add_cleanup(
            self._confd_client.groups(group).remove_extension,
            extension
        )

    def get_by(self, **kwargs):
        group = self.find_by(**kwargs)
        if not group:
            raise Exception('Group not found: {}'.format(kwargs))
        return group

    def find_by(self, **kwargs):
        groups = self._confd_client.groups.list(**kwargs)['items']
        for group in groups:
            return group
