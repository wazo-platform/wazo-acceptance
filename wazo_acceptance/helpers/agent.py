# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later


class Agent:

    def __init__(self, context):
        self._context = context
        self._confd_client = context.confd_client

    def create(self, body):
        agent = self._confd_client.agents.create(body)
        self._context.add_cleanup(self._confd_client.agents.delete, agent)
        return agent

    def get_by(self, **kwargs):
        agent = self._find_by(**kwargs)
        if not agent:
            raise Exception('Agent not found: {}'.format(kwargs))
        return agent

    def _find_by(self, **kwargs):
        agents = self._confd_client.agents.list(**kwargs)['items']
        for agent in agents:
            return agent
