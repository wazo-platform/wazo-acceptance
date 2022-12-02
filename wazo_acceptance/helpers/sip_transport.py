# Copyright 2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later


class SIPTransport:

    def __init__(self, context):
        self._context = context
        self._confd_client = context.confd_client

    def get_by(self, **kwargs):
        transport = self._find_by(**kwargs)
        if not transport:
            raise Exception(f'SIP Transport not found: {kwargs}')
        return transport

    def _find_by(self, **kwargs):
        transports = self._confd_client.sip_transports.list(**kwargs)['items']
        for transport in transports:
            return transport

    def update(self, body):
        with self._context.helpers.bus.wait_for_asterisk_reload(pjsip=True):
            self._confd_client.sip_transports.update(body)

    def update_options(self, sip_transport, new_option, value):
        options = sip_transport['options']
        new_options = [[name, value] for name, value in options if name != new_option]
        new_options.append([new_option, value])
        sip_transport['options'] = new_options
