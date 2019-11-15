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

    def create_node(self, application_uuid, call_ids):
        return self._calld_client.applications.create_node(application_uuid, call_ids)

    def get_by(self, **kwargs):
        application = self.find_by(**kwargs)
        if not application:
            raise Exception('Application not found: {}'.format(kwargs))
        return application

    def find_by(self, **kwargs):
        applications = self._confd_client.applications.list(**kwargs)['items']
        for application in applications:
            return application

    def join_node(self, application_uuid, node_uuid, exten, context):
        return self._calld_client.applications.join_node(
            application_uuid, node_uuid, exten, context,
        )

    def list_calls(self, app_uuid):
        return self._calld_client.applications.list_calls(app_uuid)['items']
