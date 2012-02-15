# -*- coding: utf-8 -*-

from lettuce.decorators import step
from lettuce.registry import world

from xivo_lettuce.common import *
from xivo_lettuce.manager.user_manager import *
from xivo_lettuce.manager.context_manager import *
from xivo_lettuce.manager import line_manager


@step(u'Given there is no user "([^"]*)" "([^"]*)"')
def given_there_is_no_user(step, firstname, lastname):
    delete_user(firstname, lastname)


@step(u'Given there is a user "([^"]*)" "([^"]*)"$')
def given_there_is_a_user_1_2(step, firstname, lastname):
    delete_user(firstname, lastname)
    insert_user(firstname, lastname)


@step(u'I add a user$')
def i_add_a_user(step):
    open_add_user_form()


@step(u'When I create a user "([^"]*)" "([^"]*)"$')
def when_i_create_a_user(step, firstname, lastname):
    open_add_user_form()
    type_user_names(firstname, lastname)
    submit_form()


@step(u'Then user "([^"]*)" "([^"]*)" is displayed in the list')
def then_user_is_displayed_in_the_list(step, firstname, lastname):
    assert user_is_saved(firstname, lastname)


@step(u'Then user "([^"]*)" "([^"]*)" is not displayed in the list')
def then_user_is_not_displayed_in_the_list(step, firstname, lastname):
    assert not user_is_saved(firstname, lastname)


@step(u'When I add user "([^"]*)" "([^"]*)" in group "([^"]*)"')
def when_i_create_a_user_in_group(step, firstname, lastname, group):
    import group_steps as grp
    grp.when_i_create_group(step, group)
    open_add_user_form()
    type_user_names(firstname, lastname)
    type_user_in_group(group)
    submit_form()
    user_is_saved(firstname, lastname)


@step(u'When I rename "([^"]*)" "([^"]*)" to "([^"]*)" "([^"]*)"')
def when_i_rename_user(step, orig_firstname, orig_lastname, dest_firstname, dest_lastname):
    id = find_user_id(orig_firstname, orig_lastname)
    delete_user(dest_firstname, dest_lastname)
    if len(id) > 0:
        open_edit_user_form(id[0])
        type_user_names(dest_firstname, dest_lastname)
        submit_form()


@step(u'When user "([^"]*)" "([^"]*)" is removed')
def remove_user(step, firstname, lastname):
    remove_line('%s %s' % (firstname, lastname))


@step(u'Then "([^"]*)" "([^"]*)" is in group "([^"]*)"')
def then_user_is_in_group(step, firstname, lastname, group_name):
    user_id_list = find_user_id(firstname, lastname)
    time.sleep(3)
    if len(user_id_list) > 0:
        assert is_in_group(group_name, user_id_list[0])


@step(u'Given a user "([^"]*)" "([^"]*)" in group "([^"]*)"')
def given_a_user_in_group(step, firstname, lastname, group):
    delete_user(firstname, lastname)
    insert_user(firstname, lastname)
    insert_group_with_user(group, find_user_id(firstname, lastname))


@step(u'Then I should be at the user list page')
def then_i_should_be_at_the_user_list_page(step):
    world.browser.find_element_by_id('bc-main', 'User list page not loaded')
    world.browser.find_element_by_name('fm-users-list')


@step(u'Given there is a user "([^"]*)" "([^"]*)" with a SIP line "([^"]*)"')
def given_there_is_a_user_1_2_with_a_sip_line_3(step, firstname, lastname, linenumber):
    check_context_number_in_interval('default', 'user', linenumber)
    delete_user(firstname, lastname)
    open_add_user_form()
    type_user_names(firstname, lastname)
    user_form_add_line(linenumber)
    submit_form()


@step(u'When I edit the line "([^"]*)"')
def when_i_edit_the_line_1(step, linenumber):
    line_manager.open_list_line_url()
    edit_line(linenumber)


@step(u'When I edit the user "([^"]*)" "([^"]*)"')
def when_i_edit_the_user_1_2(step, firstname, lastname):
    open_list_user_url()
    edit_line('%s %s' % (firstname, lastname))


@step(u'Then I see the key "([^"]*)" has the value "([^"]*)"')
def then_i_see_the_key_1_has_the_value_2(step, key, value):
    value_cell = world.browser.find_element_by_xpath(
        "//table//tr[td[@class = 'td-left' and text() = '%s']]//td[@class = 'td-right']" % key)
    assert value_cell.text == value


@step(u'I enable the XiVO Client as "([^"]*)" pass "([^"]*)" profile "([^"]*)"')
def i_enable_the_xivo_client_as_1_pass_2_profile_3(step, login, password, profile):
    step.given('Given the option "Enable XiVO Client" is checked')
    step.given('I set the text field "Login" to "%s"' % login)
    step.given('I set the text field "Password" to "%s"' % password)
    step.given('I set the select field "Profile" to "%s"' % profile)

@step(u'I add a SIP line "([^"]*)" to the user')
def given_i_add_a_sip_line_1(step, linenumber):
    user_form_add_line(linenumber)

@step(u'I add a voicemail "([^"]*)"')
def i_add_a_voicemail_1_on_2(step, vm_num):
    go_to_tab('Voicemail')
    step.given('I set the select field "Voice Mail" to "Asterisk"')
    step.given('Given the option "Enable voicemail" is checked')
    step.given('I set the text field "Voicemail" to "%s"' % vm_num)
