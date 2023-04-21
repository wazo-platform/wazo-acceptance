# Copyright 2019-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

_UNDEFINED = object()


class Call:

    def __init__(self, context):
        self._context = context
        self._calld_client = context.calld_client

    def get_by(self, **kwargs):
        call = self.find_by(**kwargs)
        if not call:
            raise Exception(f'Call not found: {kwargs}')
        return call

    def stop_recording(self, call_id):
        self._calld_client.calls.stop_record(call_id)

    def start_recording(self, call_id):
        self._calld_client.calls.start_record(call_id)

    def find_by(self, **kwargs):
        user_uuid = kwargs.pop('user_uuid', _UNDEFINED)
        caller_id_number = kwargs.pop('caller_id_number', _UNDEFINED)
        caller_id_name = kwargs.pop('caller_id_name', _UNDEFINED)
        calls = self._calld_client.calls.list_calls(**kwargs)['items']
        for call in calls:
            if user_uuid is not _UNDEFINED:
                if user_uuid != call['user_uuid']:
                    continue
            if caller_id_number is not _UNDEFINED:
                if caller_id_number != call['caller_id_number']:
                    continue
            if caller_id_name is not _UNDEFINED:
                if caller_id_name != call['caller_id_name']:
                    continue
            return call
