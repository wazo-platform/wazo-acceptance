# -*- coding: utf-8 -*-
# Copyright 2016-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from lettuce import step

from xivo_acceptance.helpers import agent_helper


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


@step(u'When I unlog agent "([^"]*)"$')
def when_i_unlog_agent_group1(step, agent_number):
    agent_helper.logoff_agent(agent_number)


@step(u'When I unlog agent "([^"]*)", ignoring errors$')
def when_i_unlog_agent_group1_ignoring_errors(step, agent_number):
    agent_helper.logoff_agent(agent_number, ignore_error=True)


@step(u'When I pause agent "([^"]*)"')
def when_i_pause_agent_1(step, agent_number):
    agent_helper.pause_agent(agent_number)


@step(u'When I unpause agent "([^"]*)"')
def when_i_unpause_agent_1(step, agent_number):
    agent_helper.unpause_agent(agent_number)
