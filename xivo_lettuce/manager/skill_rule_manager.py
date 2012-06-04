# -*- coding: utf-8 -*-

from xivo_lettuce.common import get_webservices

WSA = get_webservices('skill_rule')

def delete(skill_rule_name):
    id = find_skill_rule_id(skill_rule_name)



def find_skill_rule_id(skill_rule_name):
    skill_rule_list = WSA.search(skill_rule_name)
    print skill_rule_list
