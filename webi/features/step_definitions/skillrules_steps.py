# -*- coding: utf-8 -*-

from lettuce.decorators import step
from xivo_lettuce.manager import skill_rule_manager
from xivo_lettuce.common import open_url


@step(u'Given I remove skill rule "([^"]*)"')
def given_i_remove_skill_rule(step, skill_rule_name):
    skill_rule_manager.delete(skill_rule_name)

@step(u'When I create a skill rule "([^"]*)"')
def when_i_create_a_skill_rule(step, skill_rule_name):
    open_url('skill_rule', 'add')
    skill_rule_manager.type_skill_rule_name(skill_rule_name)

@step(u'When I add a rule "([^"]*)"')
def when_i_add_a_rule(step, rule):
    skill_rule_manager.add_rule(rule)

@step(u'Then "([^"]*)" is displayed in the list')
def then_skill_rule_is_displayed_in_the_list(step, skill_rule_content):
    assert skill_rule_manager.is_displayed(skill_rule_content)
