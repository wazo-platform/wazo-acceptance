# Copyright 2019-2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later


class Line:

    def __init__(self, context):
        self._context = context
        self._confd_client = context.confd_client

    def create(self, body):
        with self._context.helpers.bus.wait_for_asterisk_reload(dialplan=True, pjsip=True):
            line = self._confd_client.lines.create(body)
        self._context.add_cleanup(self._confd_client.lines.delete, line)
        return line

    def add_application(self, line, application):
        self._confd_client.lines(line).add_application(application)
        self._context.add_cleanup(self._confd_client.lines(line).remove_application, application)

    def add_device(self, line, device):
        self._confd_client.lines(line).add_device(device)
        self._context.add_cleanup(self._confd_client.lines(line).remove_device, device)

    def add_endpoint_sip(self, line, sip):
        with self._context.helpers.bus.wait_for_asterisk_reload(dialplan=True, pjsip=True):
            self._confd_client.lines(line).add_endpoint_sip(sip)
        self._context.add_cleanup(self._confd_client.lines(line).remove_endpoint_sip, sip)

    def add_extension(self, line, extension):
        with self._context.helpers.bus.wait_for_asterisk_reload(dialplan=True, pjsip=True, queue=True):
            self._confd_client.lines(line).add_extension(extension)
        self._context.add_cleanup(self._confd_client.lines(line).remove_extension, extension)
