# -*- coding: utf-8 -*-

from xivo_lettuce.common import get_webservices

WSA = get_webservices('skill_rule')


def delete_skill_rule_with_name(skill_rule_name):
    for id in find_skill_rule_with_name(skill_rule_name):
        WSA.delete(id)


def find_skill_rule_with_name(skill_rule_name):
    skill_rule_list = WSA.search(skill_rule_name)
    if skill_rule_list:
        return [skill_rule['id'] for skill_rule in skill_rule_list if
                skill_rule['name'] == skill_rule_name]
    return []
