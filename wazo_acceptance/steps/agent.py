# Copyright 2019-2023 The Wazo Authors  (see the AUTHORS file)
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
@when('I log agent "{number}" from API')
def agent_is_logged(context, number):
    user = context.helpers.agent.get_by(number=number)['users'][0]
    user = context.confd_client.users.get(user)
    exten = user['lines'][0]['extensions'][0]['exten']
    exten_context = user['lines'][0]['extensions'][0]['context']

    expected_event = {
        'status': 'logged_in',
    }
    with context.helpers.bus.wait_for_event('agent_status_update', expected_event):
        context.agentd_client.agents.login_agent_by_number(number, exten, exten_context)


@when('I unlog agent "{number}" from API')
def when_agent_is_unlogged(context, number):
    expected_event = {
        'status': 'logged_out',
    }
    with context.helpers.bus.wait_for_event('agent_status_update', expected_event):
        context.agentd_client.agents.logoff_agent_by_number(number)


@given('there is no queue_log for agent "{agent_number}"')
def given_no_queue_log_for_agent_1(context, agent_number):
    context.ssh_client.check_call(['queue-log-clear-one-agent.sh', agent_number])


@when('I log agent "{number}" from phone')
def when_i_log_agent_from_the_phone(context, number):
    user = context.helpers.agent.get_by(number=number)['users'][0]
    tracking_id = "{} {}".format(user['firstname'], user['lastname'])
    phone = context.phone_register.get_phone(tracking_id)
    phone.call(f'*31{number}')


@when('I unlog agent "{number}" from phone')
def when_i_unlog_agent_from_the_phone(context, number):
    user = context.helpers.agent.get_by(number=number)['users'][0]
    tracking_id = "{} {}".format(user['firstname'], user['lastname'])
    phone = context.phone_register.get_phone(tracking_id)
    phone.call(f'*32{number}')


@when('I toggle agent "{number}" status from phone')
def when_i_toggle_agent_status_from_the_phone(context, number):
    user = context.helpers.agent.get_by(number=number)['users'][0]
    tracking_id = "{} {}".format(user['firstname'], user['lastname'])
    phone = context.phone_register.get_phone(tracking_id)
    phone.call(f'*30{number}')


@when('I pause agent "{number}"')
def when_i_pause_agent_1(context, number):
    context.agentd_client.agents.pause_agent_by_number(number)


@when('I unpause agent "{number}"')
def when_i_unpause_agent_1(context, number):
    context.agentd_client.agents.unpause_agent_by_number(number)


@then('the agent "{number}" is logged')
def then_the_agent_is_logged(context, number):
    logged = context.agentd_client.agents.get_agent_status_by_number(number).logged
    assert_that(logged)


@then('the agent "{number}" is not logged')
def then_the_agent_is_not_logged(context, number):
    logged = context.agentd_client.agents.get_agent_status_by_number(number).logged
    assert_that(not_(logged))


@then('queue_log contains {expected_count} "{event_name}" events for agent "{agent_number}"')
def then_queue_log_contains_1_2_events_for_agent_3(context, expected_count, event_name, agent_number):
    actual_count = context.ssh_client.out_call(['queue-log-count-agent-events.sh', agent_number, event_name]).strip()
    assert actual_count == expected_count, f'expected {repr(expected_count)}, got {repr(actual_count)}'
