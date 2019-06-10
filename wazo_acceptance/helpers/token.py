# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from wazo_auth_client import Client as AuthClient


class Token:

    def __init__(self, context):
        self._context = context

    def create(self, username, password):
        auth_client = AuthClient(
            username=self._context.username,
            password=self._context.password,
            **self._context.wazo_config['auth']
        )

        token_data = auth_client.token.new()
        self._context.add_cleanup(auth_client.token.revoke, token_data['token'])
        return token_data
