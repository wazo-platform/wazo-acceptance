# -*- coding: utf-8 -*-

import time

from lettuce import step
from lettuce.registry import world
from selenium.webdriver.support.select import Select
from xivo_lettuce.manager import user_manager, line_manager
from xivo_lettuce.manager_ws import user_manager_ws, group_manager_ws, \
    line_manager_ws, agent_manager_ws, voicemail_manager_ws
from xivo_lettuce import common, func, form


@step(u'Given there is a user "([^"]*)" "([^"]*)"$')
def given_there_is_a_user(step, firstname, lastname):
    user_data = {
        'firstname': firstname,
        'lastname': lastname
    }
    user_manager_ws.add_or_replace_user(user_data)


@step(u'Given there is a user "([^"]*)" "([^"]*)" with extension "([^"]*)"$')
def given_there_is_a_user_with_extension(step, firstname, lastname, extension):
    number, context = func.extract_number_and_context_from_extension(extension)
    voicemail_manager_ws.delete_voicemails_with_number(number)
    user_data = {
        'firstname': firstname,
        'lastname': lastname,
        'line_context': context,
        'line_number': number
    }
    user_manager_ws.add_or_replace_user(user_data)


@step(u'Given there is a user "([^"]*)" "([^"]*)" with extension "([^"]+)@([^"]+)" and voicemail$')
def given_there_is_a_user_1_2_with_extension_3_4_and_voicemail(step, firstname, lastname, extension, context):
    voicemail_manager_ws.delete_voicemails_with_number(extension)
    user_data = {
        'firstname': firstname,
        'lastname': lastname,
        'line_context': context,
        'line_number': extension,
        'language': 'en_US',
        'voicemail_name': extension,
        'voicemail_number': extension,
    }
    user_manager_ws.add_or_replace_user(user_data)


@step(u'Given there is a user "([^"]*)" "([^"]*)" with extension "([^"]*)" in group "([^"]*)"$')
def given_there_is_a_user_with_a_sip_line_in_group(step, firstname, lastname, extension, group_name):
    number, context = func.extract_number_and_context_from_extension(extension)
    voicemail_manager_ws.delete_voicemails_with_number(number)
    user_data = {
        'firstname': firstname,
        'lastname': lastname,
        'line_context': context,
        'line_number': number
    }
    user_id = user_manager_ws.add_or_replace_user(user_data)
    group_manager_ws.add_or_replace_group(group_name, user_ids=[user_id])


@step(u'Given there is a user "([^"]*)" "([^"]*)" with CTI profile "([^"]*)"$')
def given_there_is_a_user_with_cti_profile(step, firstname, lastname, cti_profile):
    user_data = {
        'firstname': firstname,
        'lastname': lastname,
        'enable_client': True,
        'client_username': firstname.lower(),
        'client_password': lastname.lower(),
        'client_profile': cti_profile
    }
    user_manager_ws.add_or_replace_user(user_data)


@step(u'Given there is a user "([^"]*)" "([^"]*)" with extension "([^"]*)" and CTI profile "([^"]*)"$')
def given_there_is_a_user_with_extension_and_cti_profile(step, firstname, lastname, extension, cti_profile):
    number, context = func.extract_number_and_context_from_extension(extension)
    voicemail_manager_ws.delete_voicemails_with_number(number)
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
    user_manager_ws.add_or_replace_user(user_data)


@step(u'Given there is a user "([^"]*)" "([^"]*)" with extension "([^"]*)", voicemail and CTI profile "([^"]*)"$')
def given_i_there_is_a_user_with_extension_with_voicemail_and_cti_profile(step, firstname, lastname, extension, cti_profile):
    number, context = func.extract_number_and_context_from_extension(extension)
    voicemail_manager_ws.delete_voicemails_with_number(number)
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
    user_manager_ws.add_or_replace_user(user_data)


@step(u'Given there is a user "([^"]*)" "([^"]*)" with an agent "([^"]*)" and CTI profile "([^"]*)"$')
def given_there_is_a_user_with_an_agent_and_cti_profile(step, firstname, lastname, number_at_context, cti_profile):
    user_manager_ws.delete_users_with_firstname_lastname(firstname, lastname)
    number, context = number_at_context.split('@', 1)[:]
    line_manager_ws.delete_lines_with_number(number, context)
    agent_manager_ws.delete_agents_with_number(number)
    user_data = {'firstname': firstname,
                 'lastname': lastname,
                 'enable_client': True,
                 'client_username': firstname.lower(),
                 'client_password': lastname.lower(),
                 'client_profile': cti_profile,
                 'line_context': context,
                 'line_number': number,
                 }
    user_id = user_manager_ws.add_user(user_data)

    agent_data = {'firstname': firstname,
                  'lastname': lastname,
                  'number': number,
                  'context': context,
                  'users': [int(user_id)]}
    agent_manager_ws.add_agent(agent_data)


@step(u'Given there is no user "([^"]*)" "([^"]*)"$')
def given_there_is_a_no_user_1_2(step, firstname, lastname):
    user_manager_ws.delete_users_with_firstname_lastname(firstname, lastname)


@step(u'When I create a user "([^"]*)" "([^"]*)"$')
def when_i_create_a_user(step, firstname, lastname):
    common.open_url('user', 'add')
    user_manager.type_user_names(firstname, lastname)
    form.submit.submit_form()


@step(u'When I rename "([^"]*)" "([^"]*)" to "([^"]*)" "([^"]*)"$')
def when_i_rename_user(step, orig_firstname, orig_lastname, dest_firstname, dest_lastname):
    user_id = user_manager_ws.find_user_id_with_firstname_lastname(orig_firstname, orig_lastname)
    user_manager_ws.delete_users_with_firstname_lastname(dest_firstname, dest_lastname)
    common.open_url('user', 'edit', {'id': user_id})
    user_manager.type_user_names(dest_firstname, dest_lastname)
    form.submit.submit_form()


@step(u'When I remove user "([^"]*)" "([^"]*)"$')
def remove_user(step, firstname, lastname):
    common.open_url('user', 'search', {'search': '%s %s' % (firstname, lastname)})
    common.remove_line('%s %s' % (firstname, lastname))
    common.open_url('user', 'search', {'search': ''})


@step(u'When I edit the user "([^"]*)" "([^"]*)"$')
def when_i_edit_the_user_1_2(step, firstname, lastname):
    common.open_url('user', 'search', {'search': '%s %s' % (firstname, lastname)})
    common.edit_line('%s %s' % (firstname, lastname))


@step(u'When I delete agent number "([^"]*)"$')
def when_i_delete_agent_number_1(step, agent_number):
    agent = world.ws.agents.search(agent_number)[0]
    world.ws.agents.delete(agent.id)


@step(u'When I add a user "([^"]*)" "([^"]*)" with a function key with type Customized and extension "([^"]*)"$')
def when_i_add_a_user_group1_group2_with_a_function_key(step, firstname, lastname, extension):
    user_manager_ws.delete_users_with_firstname_lastname(firstname, lastname)
    common.open_url('user', 'add')
    user_manager.type_user_names(firstname, lastname)
    user_manager.type_func_key('Customized', extension)
    form.submit.submit_form()


@step(u'When I remove line from user "([^"]*)" "([^"]*)" with errors$')
def when_i_remove_line_from_user_1_2_with_errors(step, firstname, lastname):
    _edit_user(firstname, lastname)
    user_manager.remove_line()
    form.submit.submit_form_with_errors()


@step(u'When I remove line "([^"]*)" from lines then I see errors$')
def when_i_remove_line_from_lines_then_i_see_errors(step, line_number):
    common.open_url('line')
    line_manager.search_line_number(line_number)
    common.remove_line(line_number)
    form.submit.assert_form_errors()
    line_manager.unsearch_line()


@step(u'When I add a voicemail "([^"]*)" to the user "([^"]*)" "([^"]*)" with errors$')
def when_i_add_a_voicemail_1_to_the_user_2_3_with_errors(step, voicemail_number, firstname, lastname):
    _edit_user(firstname, lastname)
    user_manager.type_voicemail(voicemail_number)
    form.submit.submit_form_with_errors()


@step(u'When I add a voicemail "([^"]*)" to the user "([^"]*)" "([^"]*)"$')
def when_i_add_a_voicemail_1_to_the_user_2_3(step, voicemail_number, firstname, lastname):
    _edit_user(firstname, lastname)
    user_manager.type_voicemail(voicemail_number)
    form.submit.submit_form()


@step(u'Then "([^"]*)" "([^"]*)" is in group "([^"]*)"$')
def then_user_is_in_group(step, firstname, lastname, group_name):
    user_id = user_manager_ws.find_user_id_with_firstname_lastname(firstname, lastname)
    assert user_manager_ws.user_id_is_in_group_name(group_name, user_id)


@step(u'Then I should be at the user list page$')
def then_i_should_be_at_the_user_list_page(step):
    world.browser.find_element_by_id('bc-main', 'User list page not loaded')
    world.browser.find_element_by_name('fm-users-list')


@step(u'Then I see the user "([^"]*)" "([^"]*)" exists$')
def then_i_see_the_user_group1_group2_exists(step, firstname, lastname):
    common.open_url('user', 'search', {'search': '%s %s' % (firstname, lastname)})
    user_line = common.find_line("%s %s" % (firstname, lastname))
    assert user_line is not None
    common.open_url('user', 'search', {'search': ''})


@step(u'Then i see user with username "([^"]*)" "([^"]*)" has a function key with type Customized and extension "([^"]*)"$')
def then_i_see_user_with_username_group1_group2_has_a_function_key(step, firstname, lastname, extension):
    common.open_url('user', 'search', {'search': '%s %s' % (firstname, lastname)})
    common.edit_line("%s %s" % (firstname, lastname))
    common.go_to_tab('Func Keys')
    destination_field = world.browser.find_element_by_id('it-phonefunckey-custom-typeval-0')
    assert destination_field.get_attribute('value') == extension
    type_field = Select(world.browser.find_element_by_id('it-phonefunckey-type-0'))
    assert type_field.first_selected_option.text == "Customized"
    common.open_url('user', 'search', {'search': ''})


def _edit_user(firstname, lastname):
    user_id = user_manager_ws.find_user_id_with_firstname_lastname(firstname, lastname)
    common.open_url('user', 'edit', qry={'id': user_id})
