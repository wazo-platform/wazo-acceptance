# Copyright 2019-2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from behave import given, when, then
from hamcrest import assert_that, not_


@given('there are agents with infos')
def given_there_are_agents_with_infos(context):
    context.table.require_columns(['number'])
    for row in context.table:
        body = row.as_dict()

        context.helpers.agent.create(body)


@given('agent "{number}" is logged')
def given_agent_is_logged(context, number):
    user = context.helpers.agent.get_by(number=number)['users'][0]
    user = context.confd_client.users.get(user)
    exten = user['lines'][0]['extensions'][0]['exten']
    exten_context = user['lines'][0]['extensions'][0]['context']
    context.agentd_client.agents.login_agent_by_number(number, exten, exten_context)


@when('I log agent "{number}" from phone')
def when_i_log_agent_from_the_phone(context, number):
    user = context.helpers.agent.get_by(number=number)['users'][0]
    tracking_id = "{} {}".format(user['firstname'], user['lastname'])
    phone = context.phone_register.get_phone(tracking_id)
    phone.call('*31{number}'.format(number=number))


@when('I unlog agent "{number}" from phone')
def when_i_unlog_agent_from_the_phone(context, number):
    user = context.helpers.agent.get_by(number=number)['users'][0]
    tracking_id = "{} {}".format(user['firstname'], user['lastname'])
    phone = context.phone_register.get_phone(tracking_id)
    phone.call('*32{number}'.format(number=number))


@when('I toggle agent "{number}" status from phone')
def when_i_toggle_agent_status_from_the_phone(context, number):
    user = context.helpers.agent.get_by(number=number)['users'][0]
    tracking_id = "{} {}".format(user['firstname'], user['lastname'])
    phone = context.phone_register.get_phone(tracking_id)
    phone.call('*30{number}'.format(number=number))


@then('the agent "{number}" is logged')
def then_the_agent_is_logged(context, number):
    logged = context.agentd_client.agents.get_agent_status_by_number(number).logged
    assert_that(logged)


@then('the agent "{number}" is not logged')
def then_the_agent_is_not_logged(context, number):
    logged = context.agentd_client.agents.get_agent_status_by_number(number).logged
    assert_that(not_(logged))
