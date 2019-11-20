# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later


class AgentSkill:

    def __init__(self, context):
        self._context = context
        self._confd_client = context.confd_client

    def create(self, body):
        skill = self._confd_client.agent_skills.create(body)
        self._context.add_cleanup(self._confd_client.agent_skills.delete, skill)
        return skill

    def find_by(self, **kwargs):
        skills = self._confd_client.agent_skills.list(**kwargs)['items']
        for skill in skills:
            return skill
