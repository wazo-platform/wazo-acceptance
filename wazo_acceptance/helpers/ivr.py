# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later


class IVR:

    def __init__(self, context):
        self._context = context
        self._confd_client = context.confd_client

    def create(self, body):
        timeout = body.pop('timeout', None)
        if timeout:
            body['timeout'] = int(timeout)

        max_tries = body.pop('max_tries', None)
        if max_tries:
            body['max_tries'] = int(max_tries)

        ivr = self._confd_client.ivr.create(body)
        self._context.add_cleanup(self._confd_client.ivr.delete, ivr['id'])
        return ivr

    def get_by(self, **kwargs):
        ivr = self._find_by(**kwargs)
        if not ivr:
            raise Exception('IVR not found: {}'.format(kwargs))
        return ivr

    def _find_by(self, **kwargs):
        ivrs = self._confd_client.ivr.list(**kwargs)['items']
        for ivr in ivrs:
            return ivr
