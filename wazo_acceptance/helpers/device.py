# Copyright 2019-2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later


class Device:

    def __init__(self, context):
        self._context = context
        self._confd_client = context.confd_client

    def create(self, body):
        device = self._confd_client.devices.create(body)
        self._context.add_cleanup(self._confd_client.devices.delete, device)
        return device

    def get_by(self, **kwargs):
        device = self._find_by(**kwargs)
        if not device:
            raise Exception('Device not found: {}'.format(kwargs))
        return device

    def _find_by(self, **kwargs):
        devices = self._confd_client.devices.list(**kwargs)['items']
        for device in devices:
            return device
