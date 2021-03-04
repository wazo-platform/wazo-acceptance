# Copyright 2021 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later


class Switchboard:

    def __init__(self, context):
        self._context = context
        self._confd_client = context.confd_client
        self._calld_client = context.calld_client

    def create(self, body):
        switchboard = self._confd_client.switchboards.create(body)
        self._context.add_cleanup(self._confd_client.switchboards.delete, switchboard)
        return switchboard

    def get_by(self, **kwargs):
        switchboard = self._find_by(**kwargs)
        if not switchboard:
            raise Exception('Switchboard not found: {}'.format(kwargs))
        return switchboard

    def _find_by(self, **kwargs):
        switchboards = self._confd_client.switchboards.list(**kwargs)['items']
        for switchboard in switchboards:
            return switchboard

    def get_held_call_by(self, uuid, **kwargs):
        calls = self._calld_client.switchboards.list_held_calls(uuid)['items']
        call = self._find_call_by(calls, **kwargs)
        if not call:
            raise Exception(f'Held call from switchboard "{uuid}" not found: {kwargs}')
        return call

    def get_queued_call_by(self, uuid, **kwargs):
        calls = self._calld_client.switchboards.list_queued_calls(uuid)['items']
        call = self._find_call_by(calls, **kwargs)
        if not call:
            raise Exception(f'Queued call from switchboard "{uuid}" not found: {kwargs}')
        return call

    def _find_call_by(self, calls, **kwargs):
        caller_id_number = kwargs.get('caller_id_number', None)
        caller_id_name = kwargs.get('caller_id_name', None)
        for call in calls:
            if caller_id_number and caller_id_number != call['caller_id_number']:
                continue
            if caller_id_name and caller_id_name != call['caller_id_name']:
                continue
            return call
