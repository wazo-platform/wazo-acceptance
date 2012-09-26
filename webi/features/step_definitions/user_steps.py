# -*- coding: utf-8 -*-

import time

from lettuce import step
from lettuce.registry import world
from selenium.webdriver.support.select import Select
from xivo_lettuce import form
from xivo_lettuce.manager import user_manager, line_manager
from xivo_lettuce.manager_ws import user_manager_ws, group_manager_ws, \
    line_manager_ws, agent_manager_ws, voicemail_manager_ws
from xivo_lettuce.common import open_url, remove_line, \
    edit_line, go_to_tab, find_line
from utils import func


@step(u'Given there is a user "([^"]*)" "([^"]*)"$')
def given_there_is_a_user(step, firstname, lastname):
    user_manager_ws.delete_user_with_firstname_lastname(firstname, lastname)
    user_data = {'firstname': firstname,
                 'lastname': lastname}
    user_manager_ws.add_user(user_data)


@step(u'Given there is a user "([^"]*)" "([^"]*)" with extension "([^"]*)"$')
def given_there_is_a_user_with_extension(step, firstname, lastname, extension):
    number, context = func.extract_number_and_context_from_extension(extension)
    voicemail_manager_ws.delete_voicemail_with_number(number)
    line_manager_ws.delete_line_with_number(number, context)
    user_manager_ws.delete_user_with_firstname_lastname(firstname, lastname)
    user_data = {'firstname': firstname,
                 'lastname': lastname,
                 'line_context': context,
                 'line_number': number}
    user_manager_ws.add_user(user_data)


@step(u'Given there is a user "([^"]*)" "([^"]*)" with extension "([^"]*)" in group "([^"]*)"$')
def given_there_is_a_user_with_a_sip_line_in_group(step, firstname, lastname, extension, group_name):
    number, context = func.extract_number_and_context_from_extension(extension)
    voicemail_manager_ws.delete_voicemail_with_number(number)
    line_manager_ws.delete_line_with_number(number, context)
    user_manager_ws.delete_user_with_firstname_lastname(firstname, lastname)
    user_data = {'firstname': firstname,
                 'lastname': lastname,
                 'line_context': context,
                 'line_number': number}
    user_id = user_manager_ws.add_user(user_data)
    group_manager_ws.delete_group_with_name(group_name)
    group_manager_ws.add_group(group_name, user_ids=[user_id])


@step(u'Given there is a user "([^"]*)" "([^"]*)" with extension "([^"]*)" and CTI profile "([^"]*)"$')
def given_there_is_a_user_with_extension_and_cti_profile(step, firstname, lastname, extension, cti_profile):
    number, context = func.extract_number_and_context_from_extension(extension)
    voicemail_manager_ws.delete_voicemail_with_number(number)
    line_manager_ws.delete_line_with_number(number, context)
    user_manager_ws.delete_user_with_firstname(firstname)
    user_data = {'firstname': firstname,
                 'lastname': lastname,
                 'language': 'en_US',
                 'line_number': number,
                 'line_context': context,
                 'enable_client': True,
                 'client_username': firstname.lower(),
                 'client_password': lastname.lower(),
                 'client_profile': cti_profile
                 }
    user_manager_ws.add_user(user_data)


@step(u'Given there is a user "([^"]*)" "([^"]*)" with extension "([^"]*)", voicemail and CTI profile "([^"]*)"$')
def given_i_there_is_a_user_with_extension_with_voicemail_and_cti_profile(step, firstname, lastname, extension, cti_profile):
    number, context = func.extract_number_and_context_from_extension(extension)
    voicemail_manager_ws.delete_voicemail_with_number(number)
    line_manager_ws.delete_line_with_number(number, context)
    user_manager_ws.delete_user_with_firstname(firstname)
    user_data = {'firstname': firstname,
                 'lastname': lastname,
                 'language': 'en_US',
                 'line_number': number,
                 'line_context': context,
                 'voicemail_name': number,
                 'voicemail_number': number,
                 'enable_client': True,
                 'client_username': firstname.lower(),
                 'client_password': lastname.lower(),
                 'client_profile': cti_profile
                 }
    user_manager_ws.add_user(user_data)


@step(u'Given there is a user "([^"]*)" "([^"]*)" with an agent "([^"]*)" and CTI profile "([^"]*)"$')
def given_there_is_a_user_with_an_agent_and_cti_profile(step, firstname, lastname, agent_number, cti_profile):
    user_manager_ws.delete_user_with_firstname_lastname(firstname, lastname)
    agent_manager_ws.delete_agent_with_number(agent_number)
    user_data = {'firstname': firstname,
                 'lastname': lastname,
                 'enable_client': True,
                 'client_username': firstname.lower(),
                 'client_password': lastname.lower(),
                 'client_profile': cti_profile
                 }
    user_id = user_manager_ws.add_user(user_data)
    agent_data = {'firstname': firstname,
                  'lastname': lastname,
                  'number': agent_number,
                  'context': 'default',
                  'users': [int(user_id)]
    }
    agent_manager_ws.add_agent(agent_data)


@step(u'Given there is no user "([^"]*)" "([^"]*)"$')
def given_there_is_a_no_user_1_2(step, firstname, lastname):
    user_manager_ws.delete_user_with_firstname_lastname(firstname, lastname)


@step(u'I add a user$')
def i_add_a_user(step):
    open_url('user', 'add')


@step(u'When I create a user "([^"]*)" "([^"]*)"$')
def when_i_create_a_user(step, firstname, lastname):
    open_url('user', 'add')
    user_manager.type_user_names(firstname, lastname)
    form.submit_form()


@step(u'When I add user "([^"]*)" "([^"]*)" in group "([^"]*)"$')
def when_i_create_a_user_in_group(step, firstname, lastname, group):
    import group_steps as grp
    grp.when_i_create_group(step, group)
    open_url('user', 'add')
    user_manager.type_user_names(firstname, lastname)
    user_manager.type_user_in_group(group)
    form.submit_form()


@step(u'When I rename "([^"]*)" "([^"]*)" to "([^"]*)" "([^"]*)"')
def when_i_rename_user(step, orig_firstname, orig_lastname, dest_firstname, dest_lastname):
    id = user_manager_ws.find_user_id_with_firstname_lastname(orig_firstname, orig_lastname)
    user_manager_ws.delete_user_with_firstname_lastname(dest_firstname, dest_lastname)
    if len(id) > 0:
        open_url('user', 'edit', {'id': id[0]})
        user_manager.type_user_names(dest_firstname, dest_lastname)
        form.submit_form()


@step(u'When I remove user "([^"]*)" "([^"]*)"')
def remove_user(step, firstname, lastname):
    open_url('user', 'list')
    remove_line('%s %s' % (firstname, lastname))


@step(u'Then "([^"]*)" "([^"]*)" is in group "([^"]*)"')
def then_user_is_in_group(step, firstname, lastname, group_name):
    user_id_list = user_manager_ws.find_user_id_with_firstname_lastname(firstname, lastname)
    time.sleep(3)
    if len(user_id_list) > 0:
        assert user_manager_ws.user_id_is_in_group_name(group_name, user_id_list[0])


@step(u'Then I should be at the user list page')
def then_i_should_be_at_the_user_list_page(step):
    world.browser.find_element_by_id('bc-main', 'User list page not loaded')
    world.browser.find_element_by_name('fm-users-list')


@step(u'I edit the user "([^"]*)" "([^"]*)"')
def when_i_edit_the_user_1_2(step, firstname, lastname):
    open_url('user', 'list')
    edit_line('%s %s' % (firstname, lastname))


@step(u'I enable the XiVO Client as "([^"]*)" pass "([^"]*)" profile "([^"]*)"')
def i_enable_the_xivo_client_as_1_pass_2_profile_3(step, login, password, profile):
    step.given('Given the option "Enable XiVO Client" is checked')
    step.given('I set the text field "Login" to "%s"' % login)
    step.given('I set the text field "Password" to "%s"' % password)
    step.given('I set the select field "Profile" to "%s"' % profile)


@step(u'I add a SIP line "([^"]*)" to the user')
def given_i_add_a_sip_line_1(step, linenumber):
    user_manager.user_form_add_line(linenumber)


@step(u'I add a voicemail "([^"]*)"')
def i_add_a_voicemail_1_on_2(step, vm_num):
    go_to_tab('Voicemail')
    step.given('I set the select field "Voice Mail" to "Asterisk"')
    step.given('Given the option "Enable voicemail" is checked')
    step.given('I set the text field "Voicemail" to "%s"' % vm_num)


@step(u'When I delete agent number "([^"]*)"')
def when_i_delete_agent_number_1(step, agent_number):
    agent = world.ws.agents.search(agent_number)[0]
    world.ws.agents.delete(agent.id)

    time.sleep(world.timeout)


@step(u'When I add a user "([^"]*)" "([^"]*)" with a function key with type Customized and extension "([^"]*)"')
def when_i_add_a_user_group1_group2_with_a_function_key(step, firstname, lastname, extension):
    user_manager_ws.delete_user_with_firstname_lastname(firstname, lastname)
    open_url('user', 'add')

    user_manager.type_user_names(firstname, lastname)
    user_manager.type_func_key('Customized', extension)

    form.submit_form()


@step(u'Then I see the user "([^"]*)" "([^"]*)" exists')
def then_i_see_the_user_group1_group2_exists(step, firstname, lastname):
    open_url('user', 'list')
    user_line = find_line("%s %s" % (firstname, lastname))
    assert user_line is not None


@step(u'Then i see user with username "([^"]*)" "([^"]*)" has a function key with type Customized and extension "([^"]*)"')
def then_i_see_user_with_username_group1_group2_has_a_function_key(step, firstname, lastname, extension):
    edit_line("%s %s" % (firstname, lastname))
    go_to_tab('Func Keys')
    destination_field = world.browser.find_element_by_id('it-phonefunckey-custom-typeval-0')
    assert destination_field.get_attribute('value') == extension
    type_field = Select(world.browser.find_element_by_id('it-phonefunckey-type-0'))
    assert type_field.first_selected_option.text == "Customized"


@step(u'When I remove line "([^"]*)" from user')
def when_i_remove_line_from_user(step, lineNumber):
    go_to_tab('Lines')
    select_line = world.browser.find_element_by_xpath("//table[@id='list_linefeatures']/tbody/tr//input[@id='linefeatures-number' and @value='%s']" % lineNumber)
    delete_button = select_line.find_element_by_xpath("//a[@title='Delete this line']")
    delete_button.click()
    time.sleep(world.timeout)


@step(u'When I remove line "([^"]*)" from lines with errors')
def when_i_remove_line_from_lines(step, line_number):
    open_url('line')
    line_manager.search_line_number(line_number)
    remove_line(line_number)
    form.assert_form_errors()
    line_manager.unsearch_line()
