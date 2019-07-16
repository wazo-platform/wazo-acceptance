# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later


class User:

    def __init__(self, context):
        self._context = context
        self._auth_client = context.auth_client

    def create(self, body):
        user = self._auth_client.users.new(**body)
        self._context.add_cleanup(self._auth_client.users.delete, user['uuid'])
        return user

    def get_by(self, **kwargs):
        user = self.find_by(**kwargs)
        if not user:
            raise Exception('User not found: {}'.format(kwargs))
        return user

    def find_by(self, **kwargs):
        users = self._auth_client.users.list(**kwargs)['items']
        for user in users:
            return user

    def add(self, user, voicemail_id):
        confd_user = self._confd_client.users(user)
        confd_user.add_voicemail(voicemail_id)
        self._context.add_cleanup(confd_user.remove_voicemail)
