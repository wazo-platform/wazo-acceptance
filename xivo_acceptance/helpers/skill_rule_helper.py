# -*- coding: utf-8 -*-
# Copyright (C) 2013-2014 Avencall
# SPDX-License-Identifier: GPL-3.0+

from lettuce.registry import world


def delete_skill_rules_with_name(name):
    for skill_rule in _search_skill_rules_with_name(name):
        world.ws.queueskillrules.delete(skill_rule.id)


def _search_skill_rules_with_name(name):
    return world.ws.queueskillrules.search_by_name(name)
