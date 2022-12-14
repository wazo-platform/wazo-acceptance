# Copyright 2019-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later


class Line:

    def __init__(self, context):
        self._context = context
        self._confd_client = context.confd_client

    def create(self, body):
        modules = {'dialplan': True, 'pjsip': True}
        wait_reload = self._context.helpers.bus.wait_for_asterisk_reload
        with wait_reload(**modules):
            line = self._confd_client.lines.create(body)

        delete = self._confd_client.lines.delete
        self._context.add_cleanup(wait_reload(**modules)(delete), line)
        return line

    def add_application(self, line, application):
        self._confd_client.lines(line).add_application(application)
        self._context.add_cleanup(self._confd_client.lines(line).remove_application, application)

    def add_device(self, line, device):
        self._confd_client.lines(line).add_device(device)
        self._context.add_cleanup(self._confd_client.lines(line).remove_device, device)

    def add_endpoint_sip(self, line, sip):
        self._confd_client.lines(line).add_endpoint_sip(sip)
        remove = self._confd_client.lines(line).remove_endpoint_sip
        self._context.add_cleanup(remove, sip)

    def add_extension(self, line, extension):
        modules = {'dialplan': True, 'pjsip': True, 'queue': True}
        wait_reload = self._context.helpers.bus.wait_for_asterisk_reload
        with wait_reload(**modules):
            self._confd_client.lines(line).add_extension(extension)

        remove = self._confd_client.lines(line).remove_extension
        self._context.add_cleanup(wait_reload(**modules)(remove), extension)
