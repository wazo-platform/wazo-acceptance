# Copyright 2019-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from requests import HTTPError


class ConfdUser:

    def __init__(self, context):
        self._context = context
        self._confd_client = context.confd_client

    def create(self, body):
        ring_seconds = body.pop('ring_seconds', None)
        if ring_seconds:
            body['ring_seconds'] = int(ring_seconds)

        recording_fields = [
            'call_record_outgoing_internal_enabled',
            'call_record_incoming_internal_enabled',
            'call_record_outgoing_external_enabled',
            'call_record_incoming_external_enabled',
        ]
        for field in recording_fields:
            record_enabled = body.pop(field, None)
            if record_enabled:
                body[field] = record_enabled == 'yes'

        modules = {'dialplan': True, 'pjsip': True, 'queue': True}
        wait_reload = self._context.helpers.bus.wait_for_asterisk_reload
        with wait_reload(**modules):
            user = self._confd_client.users.create(body)

        delete = self._confd_client.users.delete
        self._context.add_cleanup(wait_reload(**modules)(delete), user)
        return user

    def add_line(self, user, line):
        modules = {'dialplan': True, 'pjsip': True}
        wait_reload = self._context.helpers.bus.wait_for_asterisk_reload
        with wait_reload(**modules):
            self._confd_client.users(user).add_line(line)

        remove = self._confd_client.users(user).remove_line
        self._context.add_cleanup(wait_reload(**modules)(remove), line)

    def add_voicemail(self, user, voicemail):
        modules = {'pjsip': True}
        wait_reload = self._context.helpers.bus.wait_for_asterisk_reload
        with wait_reload(**modules):
            self._confd_client.users(user).add_voicemail(voicemail)

        remove = self._confd_client.users(user).remove_voicemail
        self._context.add_cleanup(wait_reload(**modules)(remove))

    def update_fallback(self, user, fallback):
        fallbacks = self._confd_client.users(user).list_fallbacks()
        fallbacks.update(fallback)
        self._confd_client.users(user).update_fallbacks(fallbacks)

    def set_ringing_time(self, user, ringing_time):
        user.pop('call_record_enabled', None)
        user.update({'ring_seconds': ringing_time})
        self._confd_client.users.update(user)

    def get_by(self, **kwargs):
        user = self._find_by(**kwargs)
        if not user:
            raise Exception('Confd user not found: {}'.format(kwargs))
        return user

    def import_users(self, csv):
        try:
            return self._confd_client.users.import_csv(csv)
        except HTTPError as e:
            return e.response

    def _find_by(self, **kwargs):
        users = self._confd_client.users.list(**kwargs)['items']
        for user in users:
            return user

    def update_funckeys(self, user, func_keys):
        with self._context.helpers.bus.wait_for_asterisk_reload(dialplan=True):
            self._confd_client.users(user).update_funckeys(func_keys)
