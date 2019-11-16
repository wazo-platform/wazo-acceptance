# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later


class Schedule:

    def __init__(self, context):
        self._context = context
        self._confd_client = context.confd_client

    def create(self, body):
        schedule = self._confd_client.schedules.create(body)
        self._context.add_cleanup(self._confd_client.schedules.delete, schedule)
        return schedule

    def get_by(self, **kwargs):
        schedule = self._find_by(**kwargs)
        if not schedule:
            raise Exception('Schedule not found: {}'.format(kwargs))
        return schedule

    def _find_by(self, **kwargs):
        schedules = self._confd_client.schedules.list(**kwargs)['items']
        for schedule in schedules:
            return schedule
