# -*- coding: utf-8 -*-

# Copyright (C) 2013 Avencall
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

from lettuce.decorators import step

from xivo_acceptance.action.webi import skill_rule as skill_rule_action_webi
from xivo_acceptance.helpers import skill_rule_helper
from xivo_lettuce import common, form


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
