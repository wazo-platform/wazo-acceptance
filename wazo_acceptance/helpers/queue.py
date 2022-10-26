# Copyright 2019-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later


class Queue:

    def __init__(self, context):
        self._context = context
        self._confd_client = context.confd_client

    def create(self, body):
        options = body.pop('options', [])

        strategy = body.pop('strategy', None)
        if strategy is not None:
            options.append(('strategy', strategy))

        retry = body.pop('retry', None)
        if retry is not None:
            options.append(('retry', retry))

        retry_on_timeout = body.pop('retry_on_timeout', None)
        if isinstance(retry_on_timeout, str):
            body['retry_on_timeout'] = retry_on_timeout.lower() == 'true'

        if options:
            body['options'] = options

        modules = {'queue': True}
        wait_reload = self._context.helpers.bus.wait_for_asterisk_reload
        with wait_reload(**modules):
            queue = self._confd_client.queues.create(body)

        delete = self._confd_client.queues.delete
        self._context.add_cleanup(wait_reload(**modules)(delete), queue)
        return queue

    def add_extension(self, queue, extension):
        modules = {'dialplan': True}
        wait_reload = self._context.helpers.bus.wait_for_asterisk_reload
        with wait_reload(**modules):
            self._context.confd_client.queues(queue).add_extension(extension)

        remove = self._confd_client.queues(queue).remove_extension
        self._context.add_cleanup(wait_reload(**modules)(remove), extension)

    def add_agent_member(self, queue, agent, penalty=0):
        penalty = int(penalty)
        self._context.confd_client.queues(queue).add_agent_member(agent, penalty=penalty)
        self._context.add_cleanup(
            self._confd_client.queues(queue).remove_agent_member, agent
        )

    def add_user_member(self, queue, user):
        modules = {'pjsip': True, 'queue': True}
        wait_reload = self._context.helpers.bus.wait_for_asterisk_reload
        with wait_reload(**modules):
            self._context.confd_client.queues(queue).add_user_member(user)

        remove = self._confd_client.queues(queue).remove_user_member
        self._context.add_cleanup(wait_reload(**modules)(remove), user)

    def get_by(self, **kwargs):
        queue = self.find_by(**kwargs)
        if not queue:
            raise Exception('Queue not found: {}'.format(kwargs))
        return queue

    def find_by(self, **kwargs):
        queues = self._confd_client.queues.list(**kwargs)['items']
        for queue in queues:
            return queue
