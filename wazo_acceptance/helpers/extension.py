# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later


class Extension:

    def __init__(self, context):
        self._context = context
        self._confd_client = context.confd_client

    def create(self, body):
        body.setdefault('context', 'default')
        extension = self._confd_client.extensions.create(body)
        self._context.add_cleanup(self._confd_client.extensions.delete, extension)
        return extension

    def get_by(self, **kwargs):
        user = self.find_by(**kwargs)
        if not user:
            raise Exception('Extension not found: {}'.format(kwargs))
        return user

    def find_by(self, **kwargs):
        extensions = self._confd_client.extensions.list(**kwargs)['items']
        for extension in extensions:
            return extension
