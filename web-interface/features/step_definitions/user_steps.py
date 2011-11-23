# -*- coding: utf-8 -*-

from lettuce.decorators import step
from lettuce.registry import world
from selenium.common.exceptions import NoSuchElementException

from common.common import submit_form
from ipbx_objects.user_manager import *


@step(u'Given there is no user (.*) (.*)')
def given_there_is_no_user(step, firstname, lastname):
    delete_user(firstname, lastname)

@step(u'When I create a user (.*) ([a-zA-Z-]+)$')
def when_i_create_a_user(step, firstName, lastName):
    open_add_user_form()
    type_user_names(firstName, lastName)
    submit_form()

@step(u'Then user (.*) (.*) is displayed in the list')
def then_user_is_displayed_in_the_list(step, firstname, lastname):
    assert user_is_saved(firstname, lastname)

@step(u'Then user (.*) (.*) is not displayed in the list')
def then_user_is_not_displayed_in_the_list(step, firstname, lastname):
    assert not user_is_saved(firstname, lastname)

@step(u'When I add user (.*) (.*) in group (.*)')
def when_i_create_a_user_in_group(step, firstname, lastname, group):
    import context_steps as ctx
    ctx.when_i_edit_a_context(step, 'default')
    ctx.when_i_edit_group_ranges(step)
    ctx.when_i_add_group_interval(step, 5000, 6000)
    import group_steps as grp
    grp.when_i_create_group(step, group)
    open_add_user_form()
    type_user_names(firstname, lastname)
    type_user_in_group(group)
    submit_form()
    user_is_saved(firstname, lastname)

@step(u'When I edit (.*) (.*)')
def when_i_edit_user(step, firstname, lastname):
    id = _find_user_id(firstname, lastname)
    if len(id) > 0:
        _open_edit_user_form(id[0])
        submit_form()

@step(u'When I rename (.*) (.*) to (.*) (.*)')
def when_i_rename_user(step, orig_firstname, orig_lastname, dest_firstname, dest_lastname):
    id = find_user_id(orig_firstname, orig_lastname)
    delete_user(dest_firstname, dest_lastname)
    if len(id) > 0:
        open_edit_user_form(id[0])
        type_user_names(dest_firstname, dest_lastname)
        submit_form()

@step(u'When user (.*) (.*) is removed')
def remove_user(step, firstname, lastname):
    world.wait_for_id('table-main-listing', 'Delete button not loaded')
    delete_button = world.browser.find_element_by_xpath("//table[@id='table-main-listing']//tr[contains(.,'%s %s')]//a[@title='Delete']" % (firstname, lastname))
    delete_button.click()
    alert = world.browser.switch_to_alert();
    alert.accept()

@step(u'Then (.*) (.*) is in group (.*)')
def then_user_is_in_group(step, firstname, lastname, group_name):
    user_id_list = find_user_id(firstname, lastname)
    if len(user_id_list) > 0:
        assert is_in_group(group_name, user_id_list[0])

@step(u'Given a user (.*) (.*) in group (.*)')
def given_a_user_in_group(step, firstname, lastname, group):
    delete_user(firstname, lastname)
    insert_user(firstname, lastname)
    insert_group_with_user(group, _find_user_id(firstname, lastname))

@step(u'Then I should be at the user list page')
def then_i_should_be_at_the_user_list_page(step):
    world.wait_for_id('bc-main', 'User list page not loaded')
    try:
        list = world.browser.find_element_by_name('fm-users-list')
    except:
        list = None
    assert list is not None
