# Copyright 2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later


class CallFilter:

    def __init__(self, context):
        self._context = context
        self._confd_client = context.confd_client

    def create(self, body):
        surrogates_timeout = body.pop('surrogates_timeout', None)
        if surrogates_timeout:
            body['surrogates_timeout'] = int(surrogates_timeout)

        call_filter = self._confd_client.call_filters.create(body)
        self._context.add_cleanup(self._confd_client.call_filters.delete, call_filter)
        return call_filter

    def get_by(self, **kwargs):
        call_filter = self._find_by(**kwargs)
        if not call_filter:
            raise Exception('Call Filter not found: {}'.format(kwargs))
        return call_filter

    def _find_by(self, **kwargs):
        call_filters = self._confd_client.call_filters.list(**kwargs)['items']
        for call_filter in call_filters:
            return call_filter
