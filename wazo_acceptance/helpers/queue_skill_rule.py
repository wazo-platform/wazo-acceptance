# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later


class QueueSkillRule:

    def __init__(self, context):
        self._context = context
        self._confd_client = context.confd_client

    def create(self, body):
        skill_rule = self._confd_client.queue_skill_rules.create(body)
        self._context.add_cleanup(self._confd_client.queue_skill_rules.delete, skill_rule)
        return skill_rule

    def get_by(self, **kwargs):
        skill_rule = self._find_by(**kwargs)
        if not skill_rule:
            raise Exception('Skill rule not found: {}'.format(kwargs))
        return skill_rule

    def _find_by(self, **kwargs):
        skill_rules = self._confd_client.queue_skill_rules.list(**kwargs)['items']
        for skill_rule in skill_rules:
            return skill_rule
