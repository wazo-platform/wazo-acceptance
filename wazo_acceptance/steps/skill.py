# Copyright 2019-2025 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from behave import given


@given('there are skill rules with infos:')
def given_there_are_skill_rules_with_infos(context):
    context.table.require_columns(['name', 'definition'])
    for row in context.table:
        body = row.as_dict()
        body = {'name': body['name'], 'rules': [{'definition': body['definition']}]}
        context.helpers.queue_skill_rule.create(body)


@given('there are "{skill_name}" skill rule with infos:')
def given_there_are_name_skill_rule_with_infos(context, skill_name):
    context.table.require_columns(['definition'])
    rules = [{'definition': row.get('definition')} for row in context.table]
    body = {'name': skill_name, 'rules': rules}
    context.helpers.queue_skill_rule.create(body)


@given('agent "{number}" has skill "{skill_name}" with weight "{weight}"')
def given_agent_number_has_skill_with_weight(context, number, skill_name, weight):
    agent = context.helpers.agent.get_by(number=number)

    skill = context.helpers.agent_skill.find_by(name=skill_name)
    if not skill:
        skill_body = {'name': skill_name}
        skill = context.helpers.agent_skill.create(skill_body)

    context.helpers.agent.add_skill(agent, skill, weight=weight)
