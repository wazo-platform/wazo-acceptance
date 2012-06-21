# -*- coding: utf-8 -*-

import time
from lettuce.decorators import step
from lettuce.registry import world

from xivo_lettuce.common import *
from xivo_lettuce.manager import user_manager as user_man
from xivo_lettuce.manager import context_manager as ctx_man
from xivo_lettuce.manager import line_manager as line_man


@step(u'Given there is a user "([^"]*)" "([^"]*)"$')
def given_there_is_a_user_1_2(step, firstname, lastname):
    user_man.delete_user(firstname, lastname)
    user_man.insert_user(firstname, lastname)


@step(u'Given there is a user "([^"]*)" "([^"]*)" with no line$')
def given_there_is_a_user_1_2_with_no_line(step, firstname, lastname):
    user_man.delete_user(firstname, lastname)
    user_man.insert_user_with_no_line(firstname, lastname)


@step(u'Given there is no user "([^"]*)" "([^"]*)"$')
def given_there_is_a_no_user_1_2(step, firstname, lastname):
    user_man.delete_user(firstname, lastname)


@step(u'I add a user$')
def i_add_a_user(step):
    open_url('user', 'add')


@step(u'When I create a user "([^"]*)" "([^"]*)"$')
def when_i_create_a_user(step, firstname, lastname):
    open_url('user', 'add')
    user_man.type_user_names(firstname, lastname)
    submit_form()


@step(u'When I add user "([^"]*)" "([^"]*)" in group "([^"]*)"')
def when_i_create_a_user_in_group(step, firstname, lastname, group):
    import group_steps as grp
    grp.when_i_create_group(step, group)
    open_url('user', 'add')
    user_man.type_user_names(firstname, lastname)
    user_man.type_user_in_group(group)
    submit_form()
    element_is_in_list('user', '%s %s' % (firstname, lastname))


@step(u'When I rename "([^"]*)" "([^"]*)" to "([^"]*)" "([^"]*)"')
def when_i_rename_user(step, orig_firstname, orig_lastname, dest_firstname, dest_lastname):
    id = user_man.find_user_id(orig_firstname, orig_lastname)
    user_man.delete_user(dest_firstname, dest_lastname)
    if len(id) > 0:
        open_url('user', 'edit', {'id': id[0]})
        user_man.type_user_names(dest_firstname, dest_lastname)
        submit_form()


@step(u'When I remove user "([^"]*)" "([^"]*)"')
def remove_user(step, firstname, lastname):
    remove_line('%s %s' % (firstname, lastname))


@step(u'Then "([^"]*)" "([^"]*)" is in group "([^"]*)"')
def then_user_is_in_group(step, firstname, lastname, group_name):
    user_id_list = user_man.find_user_id(firstname, lastname)
    time.sleep(3)
    if len(user_id_list) > 0:
        assert user_man.is_in_group(group_name, user_id_list[0])


@step(u'Given a user "([^"]*)" "([^"]*)" in group "([^"]*)"')
def given_a_user_in_group(step, firstname, lastname, group):
    user_man.delete_user(firstname, lastname)
    user_man.insert_user(firstname, lastname)
    user_man.insert_group_with_user(group, user_man.find_user_id(firstname, lastname))


@step(u'Then I should be at the user list page')
def then_i_should_be_at_the_user_list_page(step):
    world.browser.find_element_by_id('bc-main', 'User list page not loaded')
    world.browser.find_element_by_name('fm-users-list')


@step(u'Given there is a user "([^"]*)" "([^"]*)" with a SIP line "([^"]*)"')
def given_there_is_a_user_1_2_with_a_sip_line_3(step, firstname, lastname, linenumber):
    ctx_man.check_context_number_in_interval('default', 'user', linenumber)
    user_man.delete_user(firstname, lastname)
    open_url('user', 'add')
    user_man.type_user_names(firstname, lastname)
    user_man.user_form_add_line(linenumber)
    submit_form()


@step(u'Given there is a user "([^"]*)" "([^"]*)" with a SIP line "([^"]*)" in group "([^"]*)"')
def given_there_is_a_user_1_2_with_a_sip_line_3_in_group_4(step, firstname, lastname, linenumber, group_name):
    ctx_man.check_context_number_in_interval('default', 'user', linenumber)
    user_man.delete_user(firstname, lastname)
    open_url('user', 'add')
    user_man.type_user_names(firstname, lastname)
    user_man.type_user_in_group(group_name)
    user_man.user_form_add_line(linenumber)
    submit_form()


@step(u'When I edit the line "([^"]*)"')
def when_i_edit_the_line_1(step, linenumber):
    line_ids = line_man.find_line_id_from_number(linenumber)
    if len(line_ids) > 0:
        open_url('line', 'edit', {'id':line_ids[0]})


@step(u'I edit the user "([^"]*)" "([^"]*)"')
def when_i_edit_the_user_1_2(step, firstname, lastname):
    open_url('user', 'list')
    edit_line('%s %s' % (firstname, lastname))


@step(u'Then I see the line "([^"]*)" has its call limit to "([^"]*)"')
def then_i_see_the_line_1_has_its_call_limit_to_2(step, line_number, call_limit):
    line_id = line_man.find_line_id_from_number(line_number)[0]
    open_url('line', 'edit', {'id': line_id})

    go_to_tab('IPBX Infos')

    key = 'call_limit'
    value_cell = world.browser.find_element_by_xpath(
        "//table"
        "//tr[td[@class = 'td-left' and text() = '%s']]"
        "//td[@class = 'td-right']"
        % key)
    assert value_cell.text == call_limit


@step(u'I enable the XiVO Client as "([^"]*)" pass "([^"]*)" profile "([^"]*)"')
def i_enable_the_xivo_client_as_1_pass_2_profile_3(step, login, password, profile):
    step.given('Given the option "Enable XiVO Client" is checked')
    step.given('I set the text field "Login" to "%s"' % login)
    step.given('I set the text field "Password" to "%s"' % password)
    step.given('I set the select field "Profile" to "%s"' % profile)


@step(u'I add a SIP line "([^"]*)" to the user')
def given_i_add_a_sip_line_1(step, linenumber):
    user_man.user_form_add_line(linenumber)


@step(u'I add a voicemail "([^"]*)"')
def i_add_a_voicemail_1_on_2(step, vm_num):
    go_to_tab('Voicemail')
    step.given('I set the select field "Voice Mail" to "Asterisk"')
    step.given('Given the option "Enable voicemail" is checked')
    step.given('I set the text field "Voicemail" to "%s"' % vm_num)


