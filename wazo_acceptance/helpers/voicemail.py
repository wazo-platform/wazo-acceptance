# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later


class Voicemail:

    def __init__(self, context):
        self._context = context
        self._confd_client = context.confd_client

    def create(self, body):
        voicemail = self._confd_client.voicemails.create(body)
        self._context.add_cleanup(self._confd_client.voicemails.delete, voicemail)
        return voicemail

    def associate(self, user, voicemail_id):
        confd_user = self._confd_client.users(user)
        confd_user.add_voicemail(voicemail_id)
        self._context.add_cleanup(confd_user.remove_voicemail)
