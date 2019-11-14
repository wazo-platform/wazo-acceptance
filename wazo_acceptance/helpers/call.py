# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later


class Call:

    def __init__(self, context):
        self._context = context
        self._calld_client = context.calld_client

    def get_by(self, **kwargs):
        call = self._find_by(**kwargs)
        if not call:
            raise Exception('Call found: {}'.format(kwargs))
        return call

    def _find_by(self, **kwargs):
        user_uuid = kwargs.pop('user_uuid', None)
        calls = self._calld_client.calls.list_calls(**kwargs)['items']
        for call in calls:
            if user_uuid and user_uuid != call['user_uuid']:
                continue
            return call
