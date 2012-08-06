# -*- coding: utf-8 -*-

from lettuce import step
from xivo_lettuce.common import open_url, element_in_list_matches_field, \
    submit_form
from xivo_lettuce.manager.context_manager import check_context_number_in_interval
from xivo_lettuce.manager.group_manager import remove_group_with_number, \
    remove_group_with_name, remove_group_with_name_via_ws, type_group_name,\
    type_group_number, type_context


@step(u'Given there is no group with number "([^"]*)"')
def given_there_is_no_group_with_number(step, number):
    remove_group_with_number(number)


@step(u'Given there is no group with name "([^"]*)"')
def given_there_is_no_group_with_name(step, name):
    remove_group_with_name_via_ws(name)


@step(u'When I create a group "([^"]*)" with number "([^"]*)"')
def when_i_create_group_with_number(step, group_name, group_number):
    check_context_number_in_interval('default', 'group', group_number)
    open_url('group', 'add')
    type_group_name(group_name)
    type_group_number(group_number)
    type_context('default')
    submit_form()


@step(u'When I set a group "([^"]*)" with number "([^"]*)"')
def when_i_set_a_group_with_number_(step, group_name, group_number):
    check_context_number_in_interval('default', 'group', group_number)
    open_url('group', 'add')
    type_group_name(group_name)
    type_group_number(group_number)
    type_context('default')


@step(u'When I create a group "([^"]*)"$')
def when_i_create_group(step, group_name):
    open_url('group', 'add')
    type_group_name(group_name)
    submit_form()


@step(u'When group "([^"]*)" is removed')
def when_group_is_removed(step, group_name):
    remove_group_with_name(group_name)


@step(u'Given there is a group "([^"]*)" number "([^"]*)" with no users')
def given_there_is_a_group_1_number_2_with_no_users(step, group_name, group_number):
    step.given('Given there is no group with name "%s"' % group_name)
    step.given('When I create a group "%s" with number "%s"' % (group_name, group_number))


@step(u'Then I see a group "([^"]*)" with no users')
def then_I_see_a_group_1_with_no_users(step, group_name):
    element_in_list_matches_field('group', group_name, 'nbqmember', 0)
