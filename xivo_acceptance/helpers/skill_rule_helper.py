# -*- coding: utf-8 -*-
# Copyright 2013-2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from lettuce.registry import world


def delete_skill_rules_with_name(name):
    for skill_rule in _search_skill_rules_with_name(name):
        world.confd_client.queue_skill_rules.delete(skill_rule['id'])


def _search_skill_rules_with_name(name):
    return world.confd_client.queue_skill_rules.list(name=name)['items']
