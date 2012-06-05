# -*- coding: utf-8 -*-

from xivo_lettuce.common import get_webservices, edit_text_field
from lettuce.registry import world
from xivo_lettuce.xivobrowser import XiVOBrowser

WSA = get_webservices('skill_rule')

def delete(skill_rule_name):
    skill_rule_id = find_skill_rule_id(skill_rule_name)
    if skill_rule_id is None:
        return
    if not WSA.delete(skill_rule_id):
        raise Exception('Unable to delete skill rule %s' % skill_rule_id)


def find_skill_rule_id(skill_rule_name):
    skill_rule_list = WSA.search(skill_rule_name)
    if skill_rule_list is not None:
        for skill_rule in skill_rule_list:
            return skill_rule['id']
    return None

def type_skill_rule_name(skill_rule_name):
    edit_text_field('it-queueskillrule-name', skill_rule_name)

def add_rule(rule):
    add_button = world.browser.find_element_by_id('lnk-add-row')
    add_button.click()
    textareas = world.browser.find_elements_by_xpath("//textarea[@id='it-queueskillrule-rule']")
    textareas[len(textareas) - 2].clear()
    textareas[len(textareas) - 2].send_keys(rule)

def is_displayed(skill_rule_content):
    element = world.browser.find_elements_by_xpath("//td[text()='%s']" % skill_rule_content)
    return len(element) > 0
