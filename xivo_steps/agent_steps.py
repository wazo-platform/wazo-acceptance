# -*- coding: UTF-8 -*-

from lettuce import step
from hamcrest import assert_that, equal_to
from xivo_lettuce import form, func
from xivo_lettuce.manager import agent_manager, agent_status_manager
from xivo_lettuce.manager_ws import agent_manager_ws, user_manager_ws
from xivo_lettuce.common import open_url, remove_line
from xivo_lettuce.manager.agent_manager import is_agent_in_agent_group, \
    remove_agent_group_if_exist, get_agent_group_id, get_nb_agents_in_group, \
    select_agent_group_list
from lettuce.registry import world
from selenium.webdriver.common.action_chains import ActionChains


@step(u'Given there is a agent "([^"]+)" "([^"]*)" with extension "([^"]+)"$')
def given_there_is_a_agent_in_context_with_number(step, firstname, lastname, extension):
    number, context = func.extract_number_and_context_from_extension(extension)
    agent_manager_ws.delete_agents_with_number(number)
    agent_data = {
        'firstname': firstname,
        'lastname': lastname,
        'number': number,
        'context': context
    }
    agent_manager_ws.add_agent(agent_data)


@step(u'Given there is a logged agent "([^"]*)" "([^"]*)" with number "([^"]*)" in "([^"]*)"$')
def given_there_is_a_logged_agent_1_2_with_number_3_in_4(step, firstname, lastname, number, context):
    user_data = {
        'firstname': firstname,
        'lastname': lastname,
        'line_number': number,
        'line_context': context
    }
    user_id = user_manager_ws.add_or_replace_user(user_data)
    agent_data = {
        'firstname': firstname,
        'lastname': lastname,
        'number': number,
        'context': context,
        'users': [user_id]
    }
    agent_manager_ws.add_or_replace_agent(agent_data)
    agent_status_manager.log_agent_on_user(number)


@step(u'Given there is no agents logged')
def given_there_is_no_agents_logged(step):
    agent_status_manager.unlog_all_agents()


@step(u'When I log agent "([^"]*)"')
def when_i_log_agent_1(step, agent_number):
    agent_status_manager.log_agent_on_user(agent_number)


@step(u'When I unlog agent "([^"]*)"')
def when_i_unlog_agent_group1(step, agent_number):
    agent_status_manager.unlog_agent_from_user(agent_number)


@step(u'When I create an agent "([^"]*)" "([^"]*)" "([^"]*)"$')
def when_i_create_an_agent(step, firstname, lastname, number):
    agent_manager_ws.delete_agents_with_number(number)
    open_url('agent', 'addagent', {'group': '1'})
    agent_manager.type_agent_info(firstname, lastname, number)
    form.submit.submit_form()


@step(u'When I create an agent "([^"]*)" "([^"]*)" "([^"]*)" in group "([^"]*)"$')
def when_i_create_an_agent_in_group(step, firstname, lastname, number, agent_group):
    agent_manager_ws.delete_agents_with_number(number)
    group_id = get_agent_group_id(agent_group)
    open_url('agent', 'addagent', {'group': group_id})
    agent_manager.type_agent_info(firstname, lastname, number)
    form.submit.submit_form()


@step(u'When I search an agent "([^"]*)"')
def when_i_search_an_agent_group1(step, search):
    open_url('agent', 'listagent', {'group': '1'})
    form.input.edit_text_field_with_id('it-toolbar-search', search)
    form.submit.submit_form('it-toolbar-subsearch')


@step(u'When I remove agent "([^"]*)" "([^"]*)"')
def when_i_remove_agent(step, firstname, lastname):
    remove_line('%s %s' % (firstname, lastname))


@step(u'When I remove agent group "([^"]*)"')
def when_i_remove_agent_group(step, agent_group_name):
    remove_line(agent_group_name)


@step(u'When I remove selected agent group')
def when_i_remove_selected_agent_group(step):
    element_to_hover_over = world.browser.find_element_by_xpath("//img[@id='toolbar-bt-advanced']")
    hover = ActionChains(world.browser).move_to_element(element_to_hover_over)
    delete_href = element_to_hover_over.find_element_by_xpath("//a[@id='toolbar-advanced-menu-delete']")
    hover.move_to_element(delete_href)
    hover.click()
    hover.perform()
    alert = world.browser.switch_to_alert()
    alert.accept()


@step(u'When I change the agent "([^"]*)" password to "([^"]*)"')
def when_i_change_the_agent_password_to_group1(step, number, password):
    agent_id = agent_manager_ws.find_agent_id_with_number(number)
    open_url('agent', 'editagent', {'group': '1', 'id': agent_id})
    agent_manager.change_password(password)
    form.submit.submit_form()


@step(u'When I create an agent group "([^"]*)"')
def when_i_create_an_agent_group(step, agent_group_name):
    remove_agent_group_if_exist(agent_group_name)
    open_url('agent', 'add')
    form.input.edit_text_field_with_id('it-agentgroup-name', agent_group_name)
    form.submit.submit_form()


@step(u'When I select a list of agent group "([^"]*)"')
def when_i_select_an_agent_group(step, agent_group_list):
    open_url('agent', 'list')
    list = agent_group_list.split(',')
    select_agent_group_list(list)


@step(u'Then agent "([^"]*)" is displayed in the list of "([^"]*)" agent group')
def then_agent_group1_is_displayed_in_the_list_of_group2_agent_group(step, agent_name, agent_group):
    assert is_agent_in_agent_group(agent_group, agent_name)


@step(u'Then agent "([^"]*)" is not displayed in the list of "([^"]*)" agent group')
def then_agent_is_not_displayed_in_the_list_of_default_agent_group(step, agent_name, agent_group):
    assert not is_agent_in_agent_group(agent_group, agent_name)


@step(u'Then agent group "([^"]*)" has "([^"]*)" agents')
def then_agent_group_has_x_agents(step, agent_group, nb_agents):
    nb_agents = int(nb_agents)

    assert_that(get_nb_agents_in_group(agent_group), equal_to(nb_agents))


@step(u'Then the agent "([^"]*)" password is "([^"]*)"')
def then_the_agent_password_is(step, number, password):
    current_password = agent_manager_ws.find_agent_password_with_number(number)

    assert_that(current_password, equal_to(password))
