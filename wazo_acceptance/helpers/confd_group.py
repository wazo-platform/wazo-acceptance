# Copyright 2019-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later


class ConfdGroup:

    def __init__(self, context):
        self._context = context
        self._confd_client = context.confd_client

    def create(self, body):
        timeout = body.pop('timeout', None)
        if timeout:
            body['timeout'] = int(timeout)

        modules = {'queue': True}
        wait_reload = self._context.helpers.bus.wait_for_asterisk_reload
        with wait_reload(**modules):
            group = self._confd_client.groups.create(body)

        delete = self._confd_client.groups.delete
        self._context.add_cleanup(wait_reload(**modules)(delete), group)
        return group

    def get_by(self, **kwargs):
        group = self._find_by(**kwargs)
        if not group:
            raise Exception(f'Group not found: {kwargs}')
        return group

    def _find_by(self, **kwargs):
        groups = self._confd_client.groups.list(**kwargs)['items']
        for group in groups:
            return group

    def add_extension(self, group, extension):
        modules = {'dialplan': True}
        wait_reload = self._context.helpers.bus.wait_for_asterisk_reload
        with wait_reload(**modules):
            self._confd_client.groups(group).add_extension(extension)

        remove = self._confd_client.groups(group).remove_extension
        self._context.add_cleanup(wait_reload(**modules)(remove), extension)

    def update_fallbacks(self, group, fallbacks):
        self._confd_client.groups(group).update_fallbacks(fallbacks)

    def update_user_members(self, group, users):
        with self._context.helpers.bus.wait_for_asterisk_reload(pjsip=True, queue=True):
            self._confd_client.groups(group).update_user_members(users)

    def update_extension_members(self, group, extensions):
        with self._context.helpers.bus.wait_for_asterisk_reload(pjsip=True, queue=True):
            self._confd_client.groups(group).update_extension_members(extensions)
