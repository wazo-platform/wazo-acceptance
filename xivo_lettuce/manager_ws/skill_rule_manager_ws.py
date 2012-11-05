# -*- coding: utf-8 -*-


def delete_skill_rules_with_name(name):
    for id in _search_skill_rules_with_name(name):
        WSA.delete(id)


def _search_skill_rules_with_name(name):
    skill_rule_list = WSA.search(name)
    if skill_rule_list:
        return [skill_rule['id'] for skill_rule in skill_rule_list if
                skill_rule['name'] == name]
    return []
