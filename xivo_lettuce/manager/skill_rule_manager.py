# -*- coding: utf-8 -*-

from xivo_lettuce.common import edit_text_field
from lettuce.registry import world


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
