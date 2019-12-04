# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later


class Queue:

    def __init__(self, context):
        self._context = context
        self._confd_client = context.confd_client

    def create(self, body):
        with self._context.helpers.bus.wait_for_asterisk_reload(queue=True):
            queue = self._confd_client.queues.create(body)
        self._context.add_cleanup(self._confd_client.queues.delete, queue)
        return queue

    def add_extension(self, queue, extension):
        with self._context.helpers.bus.wait_for_asterisk_reload(dialplan=True):
            self._context.confd_client.queues(queue).add_extension(extension)
        self._context.add_cleanup(
            self._confd_client.queues(queue).remove_extension,
            extension
        )

    def add_agent_member(self, queue, agent):
        self._context.confd_client.queues(queue).add_agent_member(agent)
        self._context.add_cleanup(
            self._confd_client.queues(queue).remove_agent_member, agent
        )

    def add_user_member(self, queue, user):
        with self._context.helpers.bus.wait_for_asterisk_reload(pjsip=True, queue=True):
            self._context.confd_client.queues(queue).add_user_member(user)
        self._context.add_cleanup(
            self._confd_client.queues(queue).remove_user_member, user
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
