# -*- coding: utf-8 -*-
# Copyright (C) 2013-2014 Avencall
# SPDX-License-Identifier: GPL-3.0-or-later

from lettuce.decorators import step

from xivo_acceptance.action.webi import skill_rule as skill_rule_action_webi
from xivo_acceptance.helpers import skill_rule_helper
from xivo_acceptance.lettuce import common, form


@step(u'Given the skill rule "([^"]*)" does not exist')
def given_the_skill_rule_does_not_exist(step, skill_rule_name):
    skill_rule_helper.delete_skill_rules_with_name(skill_rule_name)


@step(u'When I create a skill rule "([^"]*)"')
def when_i_create_a_skill_rule(step, skill_rule_name):
    common.open_url('skill_rule', 'add')
    skill_rule_action_webi.type_skill_rule_name(skill_rule_name)
    skill_rule_config = step.hashes
    for skill_rule_element in skill_rule_config:
        rule = skill_rule_element['rule']
        skill_rule_action_webi.add_rule(rule)
    form.submit.submit_form()


@step(u'Then "([^"]*)" is displayed in the list')
def then_skill_rule_is_displayed_in_the_list(step, skill_rule_content):
    assert skill_rule_action_webi.is_displayed(skill_rule_content)
