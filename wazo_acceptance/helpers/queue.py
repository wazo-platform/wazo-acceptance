# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later


class Queue:

    def __init__(self, context):
        self._context = context
        self._confd_client = context.confd_client

    def create(self, body):
        with self._context.helpers.bus.wait_for_asterisk_reload(queue=True):
            queue = self._confd_client.queues.create(body)
        self._context.add_cleanup(self._confd_client.queues.delete, queue['id'])
        return queue

    def add_extension(self, queue, extension_id):
        self._context.confd_client.queues(queue).add_extension(extension_id)
        self._context.add_cleanup(
            self._confd_client.queues(queue['id']).remove_extension,
            extension_id
        )

    def add_agent_member(self, queue, agent_id):
        self._context.confd_client.queues(queue['id']).add_agent_member(agent_id)
        self._context.add_cleanup(
            self._confd_client.queues(queue['id']).remove_agent_member,
            agent_id
        )

    def add_user_member(self, queue, user_uuid):
        self._context.confd_client.queues(queue['id']).add_user_member(user_uuid)
        self._context.add_cleanup(
            self._confd_client.queues(queue['id']).remove_user_member,
            user_uuid
        )

    def get_by(self, **kwargs):
        queue = self.find_by(**kwargs)
        if not queue:
            raise Exception('Queue not found: {}'.format(kwargs))
        return queue

    def find_by(self, **kwargs):
        queues = self._confd_client.queues.list(**kwargs)['items']
        for queue in queues:
            return queue
