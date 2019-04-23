# -*- coding: utf-8 -*-
# Copyright 2016-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from hamcrest import assert_that, equal_to, instance_of
from lettuce import step, world

from xivo_acceptance.helpers import agent_helper
from xivo_acceptance.lettuce import auth
from xivo_agentd_client import Client as AgentdClient
from xivo_agentd_client.error import AgentdClientError


@step(u'Given there is a agent "([^"]+)" "([^"]*)" with number "([^"]+)"$')
def given_there_is_a_agent_in_context_with_number(step, firstname, lastname, number):
    agent_helper.delete_agents_with_number(number)
    agent_data = {
        'firstname': firstname,
        'lastname': lastname,
        'number': number,
    }
    agent_helper.add_agent(agent_data)


@step(u'Given there is no agents logged')
def given_there_is_no_agents_logged(step):
    agent_helper.unlog_all_agents()


@step(u'When I log agent "([^"]*)"$')
def when_i_log_agent_1(step, agent_number):
    agent_helper.login_agent(agent_number)


@step(u'When I log agent "([^"]*)", ignoring errors$')
def when_i_log_agent_1_ignoring_errors(step, agent_number):
    agent_helper.login_agent(agent_number, ignore_error=True)


@step(u'When I log agent "([^"]*)" from the phone$')
def when_i_log_agent_1_from_the_phone(step, agent_number):
    agent_helper.login_agent_from_phone(agent_number, step.scenario.phone_register)


@step(u'When I unlog agent "([^"]*)"$')
def when_i_unlog_agent_group1(step, agent_number):
    agent_helper.logoff_agent(agent_number)


@step(u'When I unlog agent "([^"]*)", ignoring errors$')
def when_i_unlog_agent_group1_ignoring_errors(step, agent_number):
    agent_helper.logoff_agent(agent_number, ignore_error=True)


@step(u'When I unlog agent "([^"]*)" from the phone$')
def when_i_unlog_agent_group1_from_the_phone(step, agent_number):
    agent_helper.logoff_agent_from_phone(agent_number, step.scenario.phone_register)


@step(u'When I pause agent "([^"]*)"')
def when_i_pause_agent_1(step, agent_number):
    agent_helper.pause_agent(agent_number)


@step(u'When I unpause agent "([^"]*)"')
def when_i_unpause_agent_1(step, agent_number):
    agent_helper.unpause_agent(agent_number)


@step(u'When I request the agent statuses with an invalid token')
def when_i_request_the_agent_statuses_with_an_invalid_token(step):
    agentd_client = AgentdClient(world.config['xivo_host'],
                                 token=auth.invalid_auth_token(),
                                 verify_certificate=False)
    _agentd_request(agentd_client.agents.get_agent_statuses)


def _agentd_request(fun, *args):
    world.agentd_response = None
    world.agentd_exception = None
    try:
        world.agentd_response = fun(*args)
    except Exception as e:
        world.agentd_exception = e


@step(u'Then I get an "invalid token" response from xivo-agentd')
def then_i_get_an_invalid_token_response_from_xivo_agentd(step):
    assert_that(world.agentd_exception, instance_of(AgentdClientError))
    assert_that(world.agentd_exception.error, equal_to('invalid token or unauthorized'))


@step(u'Then the agent "([^"]*)" is logged')
def then_the_agent_group1_is_logged(step, agent_number):
    assert agent_helper.is_agent_logged(agent_number)


@step(u'Then the agent "([^"]*)" is not logged')
def then_the_agent_group1_is_not_logged(step, agent_number):
    assert not agent_helper.is_agent_logged(agent_number)
