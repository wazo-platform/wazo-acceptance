# Copyright 2019-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later


class Voicemail:

    def __init__(self, context):
        self._context = context
        self._confd_client = context.confd_client

    def create(self, body):
        modules = {'voicemail': True}
        wait_reload = self._context.helpers.bus.wait_for_asterisk_reload
        with wait_reload(**modules):
            voicemail = self._confd_client.voicemails.create(body)

        delete = self._confd_client.voicemails.delete
        self._context.add_cleanup(wait_reload(**modules)(delete), voicemail)
        return voicemail
