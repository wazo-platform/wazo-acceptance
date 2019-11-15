# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later


class Application:

    def __init__(self, context):
        self._context = context
        self._calld_client = context.calld_client
        self._confd_client = context.confd_client

    def create(self, body):
        application = self._confd_client.applications.create(body)
        self._context.add_cleanup(self._confd_client.applications.delete, application['uuid'])
        return application

    def get_by(self, **kwargs):
        application = self._find_by(**kwargs)
        if not application:
            raise Exception('Application not found: {}'.format(kwargs))
        return application

    def _find_by(self, **kwargs):
        applications = self._confd_client.applications.list(**kwargs)['items']
        for application in applications:
            return application
