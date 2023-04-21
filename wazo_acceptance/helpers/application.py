# Copyright 2019-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later


class Application:

    def __init__(self, context):
        self._context = context
        self._calld_client = context.calld_client
        self._confd_client = context.confd_client

    def create(self, body):
        application = self._confd_client.applications.create(body)
        self._context.add_cleanup(self._confd_client.applications.delete, application)
        return application

    def get_by(self, **kwargs):
        application = self._find_by(**kwargs)
        if not application:
            raise Exception(f'Application not found: {kwargs}')
        return application

    def _find_by(self, **kwargs):
        applications = self._confd_client.applications.list(**kwargs)['items']
        for application in applications:
            return application

    def get_first_call(self, application_uuid):
        call = self._find_first_call(application_uuid)
        if not call:
            raise Exception(f'Call not found from application: {application_uuid}')
        return call

    def _find_first_call(self, application_uuid):
        calls = self._calld_client.applications.list_calls(application_uuid)['items']
        for call in calls:
            return call
