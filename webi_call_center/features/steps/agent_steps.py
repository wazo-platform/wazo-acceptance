# -*- coding: UTF-8 -*-

from lettuce import step
from xivo_lettuce import form
from xivo_lettuce.manager import agent_manager
from xivo_lettuce.manager_ws import agent_manager_ws
from xivo_lettuce.common import open_url, element_is_in_list, \
    remove_line, element_is_not_in_list
from utils import func


@step(u'Given an agent "([^"]*)" "([^"]*)" "([^"]*)" "([^"]*)" in group default')
def given_an_agent_in_group_default(step, firstname, lastname, number, password):
    agent_manager_ws.delete_agent_with_number(number)
    agent_data = {
        'firstname': firstname,
        'lastname': lastname,
        'number': number,
        'context': 'default',
        'password': password
    }
    agent_manager_ws.add_agent(agent_data)


@step(u'Given there is a agent "([^"]+)" "([^"]*)" with extension "([^"]+)"$')
def given_there_is_a_agent_in_context_with_number(step, firstname, lastname, extension):
    number, context = func.extract_number_and_context_from_extension(extension)
    agent_manager_ws.delete_agent_with_number(number)
    agent_data = {
        'firstname': firstname,
        'lastname': lastname,
        'number': number,
        'context': context
    }
    agent_manager_ws.add_agent(agent_data)


@step(u'Given there is no agent with number "([^"]*)"$')
def given_no_agent_number_1(step, number):
    agent_manager_ws.delete_agent_with_number(number)


@step(u'When I create an agent "([^"]*)" "([^"]*)" "([^"]*)"')
def when_i_create_an_agent(step, firstname, lastname, number):
    open_url('agent', 'addagent', {'group': '1'})
    agent_manager.type_agent_info(firstname, lastname, number)
    form.submit_form()


@step(u'When I remove agent "([^"]*)" "([^"]*)"')
def when_i_remove_agent(step, firstname, lastname):
    remove_line('%s %s' % (firstname, lastname))


@step(u'When I change the agent "([^"]*)" password to "([^"]*)"')
def when_i_change_the_agent_password_to_group1(step, number, password):
    agent_id = agent_manager_ws.get_agent_id_with_number(number)
    open_url('agent', 'editagent', {'group': '1', 'id': agent_id})
    agent_manager.change_password(password)
    form.submit_form()


@step(u'Then agent "([^"]*)" is displayed in the list of default agent group')
def then_agent_is_displayed_in_the_list_of_agent_group(step, agent):
    assert element_is_in_list('agent', agent, {'group': '1', 'search': agent}, 'listagent')
    open_url('agent', 'listagent', {'group': '1', 'search': ''})


@step(u'Then agent "([^"]*)" is not displayed in the list of default agent group')
def then_agent_is_not_displayed_in_the_list_of_default_agent_group(step, agent):
    assert element_is_not_in_list('agent', agent, {'group': '1', 'search': agent}, 'listagent')
    open_url('agent', 'listagent', {'group': '1', 'search': ''})


@step(u'Then the agent "([^"]*)" password is "([^"]*)"')
def then_the_agent_password_is(step, number, password):
    current_password = agent_manager_ws.get_agent_password_with_number(number)
    assert current_password == password, 'passord was not changed : expected : %s current %s' % (password, current_password)
