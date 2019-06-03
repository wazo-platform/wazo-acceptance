# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later


class EndpointSIPHelper:

    def __init__(self, context):
        self._context = context
        self._confd_client = context.confd_client

    def create(self, body):
        sip = self._confd_client.endpoints_sip.create(body)
        self._context.add_cleanup(self._confd_client.endpoints_sip.delete, sip)
        return sip

    def find_option(self, endpoint_sip, desired_option):
        for option, value in endpoint_sip['options']:
            if option == desired_option:
                return value
        return None
