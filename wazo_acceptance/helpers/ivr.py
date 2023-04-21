# Copyright 2019-2023 The Wazo Authors  (see the AUTHORS file)
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

        modules = {'dialplan': True}
        wait_reload = self._context.helpers.bus.wait_for_asterisk_reload
        with wait_reload(**modules):
            ivr = self._confd_client.ivr.create(body)

        delete = self._confd_client.ivr.delete
        self._context.add_cleanup(wait_reload(**modules)(delete), ivr)
        return ivr

    def get_by(self, **kwargs):
        ivr = self._find_by(**kwargs)
        if not ivr:
            raise Exception(f'IVR not found: {kwargs}')
        return ivr

    def _find_by(self, **kwargs):
        ivrs = self._confd_client.ivr.list(**kwargs)['items']
        for ivr in ivrs:
            return ivr
