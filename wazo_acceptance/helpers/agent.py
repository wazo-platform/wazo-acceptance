# Copyright 2019-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later


class Agent:

    def __init__(self, context):
        self._context = context
        self._confd_client = context.confd_client

    def create(self, body):
        modules = {'queue': True}
        wait_reload = self._context.helpers.bus.wait_for_asterisk_reload
        with wait_reload(**modules):
            agent = self._confd_client.agents.create(body)

        delete = self._confd_client.agents.delete
        self._context.add_cleanup(wait_reload(**modules)(delete), agent)
        return agent

    def add_skill(self, agent, skill, weight=None):
        weight = int(weight) if weight is not None else None
        with self._context.helpers.bus.wait_for_asterisk_reload(queue=True):
            self._confd_client.agents(agent).add_skill(skill, weight=weight)

    def get_by(self, **kwargs):
        agent = self._find_by(**kwargs)
        if not agent:
            raise Exception('Agent not found: {}'.format(kwargs))
        return agent

    def _find_by(self, **kwargs):
        agents = self._confd_client.agents.list(**kwargs)['items']
        for agent in agents:
            return agent
