# -*- coding: utf-8 -*-

from lettuce.decorators import step
from xivo_lettuce.manager import skill_rule_manager
from xivo_lettuce.manager_ws import skill_rule_manager_ws
from xivo_lettuce import common, form


@step(u'Given the skill rule "([^"]*)" does not exist')
def given_the_skill_rule_does_not_exist(step, skill_rule_name):
    skill_rule_manager_ws.delete_skill_rules_with_name(skill_rule_name)


@step(u'When I create a skill rule "([^"]*)"')
def when_i_create_a_skill_rule(step, skill_rule_name):
    common.open_url('skill_rule', 'add')
    skill_rule_manager.type_skill_rule_name(skill_rule_name)
    skill_rule_config = step.hashes
    for skill_rule_element in skill_rule_config:
        rule = skill_rule_element['rule']
        skill_rule_manager.add_rule(rule)
    form.submit.submit_form()


@step(u'Then "([^"]*)" is displayed in the list')
def then_skill_rule_is_displayed_in_the_list(step, skill_rule_content):
    assert skill_rule_manager.is_displayed(skill_rule_content)
