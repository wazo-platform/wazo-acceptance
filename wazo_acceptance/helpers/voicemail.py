# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later


class Voicemail:

    def __init__(self, context):
        self._context = context
        self._confd_client = context.confd_client

    def create(self, body):
        with self._context.helpers.bus.wait_for_asterisk_reload(voicemail=True):
            voicemail = self._confd_client.voicemails.create(body)
        self._context.add_cleanup(self._confd_client.voicemails.delete, voicemail)
        return voicemail
