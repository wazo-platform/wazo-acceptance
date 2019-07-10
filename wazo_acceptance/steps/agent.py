# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from behave import when, then
from hamcrest import assert_that, not_


@when('I log agent "{number}" from phone')
def when_i_log_agent_from_the_phone(context, number):
    user = context.confd_client.agents.list(number=number)['items'][0]['users'][0]
    tracking_id = "{} {}".format(user['firstname'], user['lastname'])
    phone = context.phone_register.get_phone(tracking_id)
    phone.call('*31{number}'.format(number=number))


@when('I unlog agent "{number}" from phone')
def when_i_unlog_agent_from_the_phone(context, number):
    user = context.confd_client.agents.list(number=number)['items'][0]['users'][0]
    tracking_id = "{} {}".format(user['firstname'], user['lastname'])
    phone = context.phone_register.get_phone(tracking_id)
    phone.call('*32{number}'.format(number=number))


@then('the agent "{number}" is logged')
def then_the_agent_is_logged(context, number):
    logged = context.agentd_client.agents.get_agent_status_by_number(number).logged
    assert_that(logged)


@then('the agent "{number}" is not logged')
def then_the_agent_is_not_logged(context, number):
    logged = context.agentd_client.agents.get_agent_status_by_number(number).logged
    assert_that(not_(logged))
